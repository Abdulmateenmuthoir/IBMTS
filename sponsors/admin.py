from django.contrib import admin

# Register your models here.
# sponsors/admin.py

from django.contrib import admin
from .models import Sponsor

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'status')
    search_fields = ('company_name', 'email')