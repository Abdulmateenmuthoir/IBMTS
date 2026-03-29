
from django.shortcuts import render, redirect
from .models import Sponsor

def sponsor_apply(request):
    if request.method == 'POST':
        Sponsor.objects.create(
            company_name=request.POST['company_name'],
            contact_person=request.POST['contact_person'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            sponsorship_tier=request.POST.get('tier'),
            message=request.POST['message'],
        )
        return redirect('sponsor_success')

    return render(request, 'sponsors/apply.html')


def sponsor_success(request):
    return render(request, 'sponsors/success.html')