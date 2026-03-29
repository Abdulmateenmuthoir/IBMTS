

from django.shortcuts import render, redirect
from .models import Attendee

def register(request):
    if request.method == 'POST':
        Attendee.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            category=request.POST['category'],
        )
        return redirect('register_success')

    return render(request, 'attendees/register.html')


def register_success(request):
    return render(request, 'attendees/success.html')