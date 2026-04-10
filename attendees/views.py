from django.shortcuts import render, redirect
from .models import Attendee
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def register(request):
    if request.method == 'POST':
        attendee = Attendee.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            category=request.POST['category'],
        )
        
        # Send Welcome Email
        html_message = render_to_string('emails/registration_confirm.html', {'attendee': attendee})
        send_mail(
            subject='Welcome to IBMTS 2026 - Registration Confirmed',
            message=f'Hello {attendee.name}, your registration for IBMTS 2026 is confirmed.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendee.email],
            fail_silently=True,
            html_message=html_message
        )

        return redirect('register_success')

    return render(request, 'attendees/register.html')


def register_success(request):
    return render(request, 'attendees/success.html')

def home(request):
    return render(request, 'home.html')