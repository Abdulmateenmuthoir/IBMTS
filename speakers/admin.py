from django.contrib import admin
from .models import Speaker

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'topic', 'status', 'created_at')
    search_fields = ('name', 'email')
