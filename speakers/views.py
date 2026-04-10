from django.shortcuts import render, redirect
from .models import Speaker
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def speaker_apply(request):
    if request.method == 'POST':
        speaker = Speaker.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            topic=request.POST['topic'],
            bio=request.POST['bio'],
            linkedin=request.POST.get('linkedin')
        )

        # Send Speaker Acknowledgement Email
        html_message = render_to_string('emails/speaker_ack.html', {'speaker': speaker})
        send_mail(
            subject='IBMTS 2026 - Speaker Application Received',
            message=f'Hello {speaker.name}, we have received your speaker application for IBMTS 2026.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[speaker.email],
            fail_silently=True,
            html_message=html_message
        )

        return redirect('speaker_success')

    return render(request, 'speakers/apply.html')


def speaker_success(request):
    return render(request, 'speakers/success.html')