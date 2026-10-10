import hashlib
import hmac
import json
import uuid
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from .models import Attendee
from speakers.models import Speaker
from sponsors.models import Sponsor
from dashboard.models import TeamMember, Testimonial

PAYSTACK_API = 'https://api.paystack.co/transaction'


def current_ticket_price():
    if timezone.localdate() <= date.fromisoformat(settings.EVENT_EARLY_BIRD_END):
        return settings.EVENT_EARLY_BIRD_PRICE, True
    return settings.EVENT_STANDARD_PRICE, False


def paystack_request(path, method='GET', payload=None):
    """Call Paystack only from the server; never expose the secret key."""
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        # Paystack's edge rejects Python's default urllib user agent.
        'User-Agent': 'IBMTS/1.0',
    }
    data = None
    if payload is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(payload).encode('utf-8')
    request = Request(f'{PAYSTACK_API}{path}', data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as error:
        # Keep provider diagnostics on the server; customer-facing views show
        # only a generic error so implementation details are never exposed.
        try:
            detail = json.loads(error.read().decode('utf-8')).get('message', '')
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = ''
        raise ValueError(f'Paystack API returned HTTP {error.code}: {detail}') from error


def send_registration_email(attendee):
    if attendee.registration_email_sent:
        return
    html_message = render_to_string('emails/registration_confirm.html', {'attendee': attendee})
    send_mail(
        subject='Welcome to IBMTS 2027 - Registration Confirmed',
        message=f'Hello {attendee.name}, your payment and registration for IBMTS 2027 are confirmed.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[attendee.email],
        fail_silently=True,
        html_message=html_message,
    )
    attendee.registration_email_sent = True
    attendee.save(update_fields=['registration_email_sent'])


def verify_payment(attendee):
    """Verify reference, amount and currency with Paystack before registration."""
    response = paystack_request(f'/verify/{attendee.payment_reference}')
    transaction = response.get('data', {})
    valid = (
        response.get('status') and transaction.get('status') == 'success'
        and transaction.get('reference') == attendee.payment_reference
        and transaction.get('currency') == 'NGN'
        and transaction.get('amount') == attendee.ticket_amount * 100
    )
    if not valid:
        attendee.payment_status = transaction.get('status', 'failed')
        attendee.save(update_fields=['payment_status'])
        return False
    if not attendee.is_paid:
        attendee.is_paid = True
        attendee.payment_status = 'paid'
        attendee.payment_transaction_id = str(transaction.get('id', ''))
        attendee.paid_at = timezone.now()
        attendee.save(update_fields=['is_paid', 'payment_status', 'payment_transaction_id', 'paid_at'])
    send_registration_email(attendee)
    return True


@never_cache
def register(request):
    price, is_early_bird = current_ticket_price()
    context = {'ticket_price': price, 'is_early_bird': is_early_bird, 'early_bird_end': settings.EVENT_EARLY_BIRD_END}
    if request.method != 'POST':
        return render(request, 'attendees/register.html', context)
    if not settings.PAYSTACK_SECRET_KEY:
        messages.error(request, 'Payments are not configured yet. Please contact the organisers.')
        return redirect('register')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    phone = request.POST.get('phone', '').strip()
    category = request.POST.get('category', '')
    if not all([name, email, phone]) or category not in dict(Attendee.CATEGORY_CHOICES):
        messages.error(request, 'Please complete all registration fields.')
        return redirect('register')

    attendee = Attendee.objects.filter(email=email).first()
    if attendee and attendee.is_paid:
        messages.info(request, 'This email address already has a confirmed registration.')
        return redirect('register')
    if attendee is None:
        attendee = Attendee(email=email)
    attendee.name, attendee.phone, attendee.category = name, phone, category
    attendee.ticket_amount, attendee.payment_status = price, 'pending'
    attendee.payment_reference = f'IBMTS-{uuid.uuid4().hex[:24]}'
    attendee.save()

    callback_url = getattr(settings, 'PAYSTACK_CALLBACK_URL', '') or request.build_absolute_uri(reverse('payment_callback'))
    payload = {
        'email': attendee.email, 'amount': str(attendee.ticket_amount * 100),
        'currency': 'NGN', 'reference': attendee.payment_reference, 'callback_url': callback_url,
        'metadata': {'attendee_id': attendee.id, 'ticket': 'IBMTS 2027'},
    }
    try:
        response = paystack_request('/initialize', method='POST', payload=payload)
        authorization_url = response.get('data', {}).get('authorization_url')
        if not response.get('status') or not authorization_url:
            raise ValueError(response.get('message', 'Could not start payment.'))
    except (HTTPError, URLError, ValueError, TimeoutError):
        messages.error(request, 'Unable to start payment. Please try again in a moment.')
        return redirect('register')
    return redirect(authorization_url)


def payment_callback(request):
    attendee = get_object_or_404(Attendee, payment_reference=request.GET.get('reference', ''))
    try:
        if verify_payment(attendee):
            return redirect('register_success')
    except (HTTPError, URLError, ValueError, TimeoutError):
        pass
    messages.error(request, 'We could not confirm your payment. If you were charged, contact the organisers with your payment reference.')
    return redirect('register')


@csrf_exempt
def paystack_webhook(request):
    if request.method != 'POST' or not settings.PAYSTACK_SECRET_KEY:
        return HttpResponseBadRequest()
    expected = hmac.new(settings.PAYSTACK_SECRET_KEY.encode(), request.body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(request.headers.get('x-paystack-signature', ''), expected):
        return HttpResponse(status=401)
    try:
        event = json.loads(request.body)
        if event.get('event') == 'charge.success':
            attendee = Attendee.objects.filter(payment_reference=event.get('data', {}).get('reference')).first()
            if attendee:
                verify_payment(attendee)
    except (json.JSONDecodeError, HTTPError, URLError, ValueError, TimeoutError):
        return HttpResponse(status=400)
    return HttpResponse(status=200)


def register_success(request):
    return render(request, 'attendees/success.html')


def home(request):
    price, is_early_bird = current_ticket_price()
    return render(request, 'home.html', {
        'ticket_price': price, 'is_early_bird': is_early_bird,
        'display_speakers': Speaker.objects.filter(display_on_site=True, status='approved'),
        'display_sponsors': Sponsor.objects.filter(display_on_site=True, status='approved'),
        'display_testimonials': Testimonial.objects.filter(display_on_site=True),
        'display_team_members': TeamMember.objects.filter(display_on_site=True),
    })
