from django.contrib import admin

# Register your models here.
# attendees/admin.py

from django.contrib import admin
from .models import Attendee

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'checked_in')
    search_fields = ('name', 'email', 'phone')