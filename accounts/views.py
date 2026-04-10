from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staff:
            return redirect('checkin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('checkin')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'accounts/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')
