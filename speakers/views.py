from django.shortcuts import render, redirect
from .models import Speaker

def speaker_apply(request):
    if request.method == 'POST':
        Speaker.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            topic=request.POST['topic'],
            bio=request.POST['bio'],
            linkedin=request.POST.get('linkedin')
        )
        return redirect('speaker_success')

    return render(request, 'speakers/apply.html')


def speaker_success(request):
    return render(request, 'speakers/success.html')