from django.contrib import admin
from .models import Speaker

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_title', 'status', 'sort_order', 'display_on_site', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('status', 'display_on_site')
    list_editable = ('sort_order', 'display_on_site')
