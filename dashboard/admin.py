from django.contrib import admin
from .models import TeamMember, Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'sort_order', 'display_on_site', 'created_at')
    list_filter = ('display_on_site',)
    list_editable = ('sort_order', 'display_on_site')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'sort_order', 'display_on_site')
    list_filter = ('display_on_site',)
    list_editable = ('sort_order', 'display_on_site')
