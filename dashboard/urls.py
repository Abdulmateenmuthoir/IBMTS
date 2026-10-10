from django.urls import path
from .views import (
    admin_dashboard, checkin, mark_checkin, search_attendees_api,
    edit_attendee, delete_attendee, update_speaker_status, add_staff, unmark_checkin, checkin_sync_api,
    create_site_content, toggle_site_content, upload_site_content
)

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('checkin/', checkin, name='checkin'),
    path('checkin/<int:id>/', mark_checkin, name='mark_checkin'),
    path('api/search/', search_attendees_api, name='search_api'),
    path('api/checkin-sync/', checkin_sync_api, name='checkin_sync_api'),
    path('dashboard/attendee/<int:id>/edit/', edit_attendee, name='edit_attendee'),
    path('dashboard/attendee/<int:id>/delete/', delete_attendee, name='delete_attendee'),
    path('dashboard/attendee/<int:id>/uncheck/', unmark_checkin, name='unmark_checkin'),
    path('dashboard/speaker/<int:id>/status/', update_speaker_status, name='update_speaker_status'),
    path('dashboard/add-staff/', add_staff, name='add_staff'),
    path('dashboard/content/<str:content_type>/create/', create_site_content, name='create_site_content'),
    path('dashboard/content/<str:content_type>/<int:item_id>/toggle/', toggle_site_content, name='toggle_site_content'),
    path('dashboard/content/<str:content_type>/upload/', upload_site_content, name='upload_site_content'),
]

