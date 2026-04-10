

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from attendees.models import Attendee
from speakers.models import Speaker
import json

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def admin_dashboard(request):
    attendees = Attendee.objects.all().order_by('-created_at')
    speakers = Speaker.objects.all().order_by('-created_at')
    staffs = User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')

    context = {
        'total_registered': attendees.count(),
        'total_checked_in': attendees.filter(checked_in=True).count(),
        'total_speakers': speakers.count(),
        'attendees': attendees,
        'speakers': speakers,
        'staffs': staffs,
    }
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(is_superadmin)
def add_staff(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists'})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=False
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
def checkin(request):
    query = request.GET.get('q', '')

    if query:
        attendees = Attendee.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        attendees = Attendee.objects.all().order_by('-created_at')

    return render(request, 'dashboard/checkin.html', {
        'attendees': attendees,
        'query': query
    })


@login_required
def mark_checkin(request, id):
    attendee = get_object_or_404(Attendee, id=id)

    if not attendee.checked_in:
        attendee.checked_in = True
        attendee.checked_in_at = timezone.now()
        attendee.save()

        # Send check-in email
        html_message = render_to_string('emails/checkin_confirm.html', {'attendee': attendee})
        send_mail(
            subject='Welcome to IBMTS 2026 - You are Checked In!',
            message=f'Hello {attendee.name}, welcome to IBMTS 2026!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendee.email],
            fail_silently=True,
            html_message=html_message
        )

    return JsonResponse({'success': True})


@user_passes_test(is_superadmin)
def unmark_checkin(request, id):
    if request.method == 'POST':
        attendee = get_object_or_404(Attendee, id=id)
        if attendee.checked_in:
            attendee.checked_in = False
            attendee.checked_in_at = None
            attendee.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def search_attendees_api(request):
    query = request.GET.get('q', '')

    attendees = Attendee.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(phone__icontains=query)
    )[:10]

    data = []

    for a in attendees:
        data.append({
            'id': a.id,
            'name': a.name,
            'email': a.email,
            'phone': a.phone,
            'checked_in': a.checked_in
        })

    return JsonResponse({'attendees': data})

@login_required
def checkin_sync_api(request):
    checked_in_ids = list(Attendee.objects.filter(checked_in=True).values_list('id', flat=True))
    total_registered = Attendee.objects.count()
    return JsonResponse({
        'checked_in_ids': checked_in_ids,
        'total_checked_in': len(checked_in_ids),
        'total_registered': total_registered
    })

@user_passes_test(is_superadmin)
def edit_attendee(request, id):
    attendee = get_object_or_404(Attendee, id=id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendee.name = data.get('name', attendee.name)
            attendee.email = data.get('email', attendee.email)
            attendee.phone = data.get('phone', attendee.phone)
            attendee.category = data.get('category', attendee.category)
            attendee.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@user_passes_test(is_superadmin)
def delete_attendee(request, id):
    if request.method == 'POST':
        attendee = get_object_or_404(Attendee, id=id)
        attendee.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@user_passes_test(is_superadmin)
def update_speaker_status(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            speaker = get_object_or_404(Speaker, id=id)
            if new_status in dict(Speaker.STATUS_CHOICES):
                speaker.status = new_status
                speaker.save()
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

