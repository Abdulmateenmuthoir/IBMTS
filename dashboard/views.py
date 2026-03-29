

from django.shortcuts import render, redirect, get_object_or_404
from attendees.models import Attendee
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse

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


def mark_checkin(request, id):
    attendee = get_object_or_404(Attendee, id=id)

    if not attendee.checked_in:
        attendee.checked_in = True
        attendee.checked_in_at = timezone.now()
        attendee.save()

    return JsonResponse({'success': True})



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

