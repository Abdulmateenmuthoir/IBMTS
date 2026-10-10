

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
from sponsors.models import Sponsor
from .models import TeamMember, Testimonial
import json

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def admin_dashboard(request):
    attendees = Attendee.objects.filter(is_paid=True).order_by('-created_at')
    speakers = Speaker.objects.all().order_by('-created_at')
    staffs = User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')
    sponsors = Sponsor.objects.order_by('-created_at')
    testimonials = Testimonial.objects.order_by('-created_at')
    team_members = TeamMember.objects.all()

    context = {
        'total_registered': attendees.count(),
        'total_checked_in': attendees.filter(checked_in=True).count(),
        'total_speakers': speakers.count(),
        'attendees': attendees,
        'speakers': speakers,
        'staffs': staffs,
        'sponsors': sponsors,
        'testimonials': testimonials,
        'team_members': team_members,
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
        attendees = Attendee.objects.filter(is_paid=True).filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        attendees = Attendee.objects.filter(is_paid=True).order_by('-created_at')

    return render(request, 'dashboard/checkin.html', {
        'attendees': attendees,
        'query': query
    })


@login_required
def mark_checkin(request, id):
    attendee = get_object_or_404(Attendee, id=id, is_paid=True)

    if not attendee.checked_in:
        attendee.checked_in = True
        attendee.checked_in_at = timezone.now()
        attendee.save()

        # Send check-in email
        html_message = render_to_string('emails/checkin_confirm.html', {'attendee': attendee})
        send_mail(
            subject='Welcome to IBMTS 2027 - You are Checked In!',
            message=f'Hello {attendee.name}, welcome to IBMTS 2027!',
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

    attendees = Attendee.objects.filter(is_paid=True).filter(
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
    checked_in_ids = list(Attendee.objects.filter(is_paid=True, checked_in=True).values_list('id', flat=True))
    total_registered = Attendee.objects.filter(is_paid=True).count()
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


@user_passes_test(is_superadmin)
def create_site_content(request, content_type):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        if content_type == 'speaker':
            item = Speaker.objects.create(
                name=data['name'], email=data.get('email', 'speaker@ibmts.local'),
                phone=data.get('phone', ''), topic=data.get('topic', ''), bio=data.get('bio', ''),
                display_title=data.get('display_title', ''), photo_url=data.get('photo_url', ''),
                status='approved', display_on_site=True,
            )
        elif content_type == 'testimonial':
            item = Testimonial.objects.create(name=data['name'], role=data['role'], quote=data['quote'], photo_url=data.get('photo_url', ''))
        elif content_type == 'team':
            item = TeamMember.objects.create(name=data['name'], role=data['role'], photo_url=data.get('photo_url', ''), sort_order=data.get('sort_order', 0))
        elif content_type == 'sponsor':
            item = Sponsor.objects.create(
                company_name=data['company_name'], contact_person=data.get('contact_person', data['company_name']),
                email=data.get('email', 'sponsor@ibmts.local'), phone=data.get('phone', ''), message='',
                sponsorship_tier=data.get('sponsorship_tier', 'Partnership'), status='approved',
                display_on_site=True, logo_url=data.get('logo_url', ''),
            )
        else:
            return JsonResponse({'success': False, 'error': 'Unknown content type'}, status=400)
        return JsonResponse({'success': True, 'id': item.id})
    except (KeyError, ValueError, TypeError) as error:
        return JsonResponse({'success': False, 'error': str(error)}, status=400)


@user_passes_test(is_superadmin)
def toggle_site_content(request, content_type, item_id):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    models = {'speaker': Speaker, 'testimonial': Testimonial, 'team': TeamMember, 'sponsor': Sponsor}
    model = models.get(content_type)
    if not model:
        return JsonResponse({'success': False}, status=404)
    item = get_object_or_404(model, id=item_id)
    item.display_on_site = not item.display_on_site
    item.save(update_fields=['display_on_site'])
    return JsonResponse({'success': True, 'display_on_site': item.display_on_site})


@user_passes_test(is_superadmin)
def upload_site_content(request, content_type):
    if request.method != 'POST':
        return redirect('admin_dashboard')
    photo = request.FILES.get('image')
    if content_type == 'speaker':
        Speaker.objects.create(name=request.POST['name'], email=request.POST.get('email') or f"speaker-{timezone.now().timestamp()}@ibmts.local", phone='', topic=request.POST.get('title', ''), bio='', display_title=request.POST.get('title', ''), image=photo, status='approved', display_on_site=True)
    elif content_type == 'testimonial':
        Testimonial.objects.create(name=request.POST['name'], role=request.POST.get('role', ''), quote=request.POST['quote'], image=photo)
    elif content_type == 'team':
        TeamMember.objects.create(name=request.POST['name'], role=request.POST.get('role', ''), image=photo)
    elif content_type == 'sponsor':
        Sponsor.objects.create(company_name=request.POST['name'], contact_person=request.POST['name'], email=request.POST.get('email') or f"sponsor-{timezone.now().timestamp()}@ibmts.local", phone='', message='', sponsorship_tier='Partnership', logo=photo, status='approved', display_on_site=True)
    return redirect('admin_dashboard')

