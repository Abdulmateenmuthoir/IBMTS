from django.urls import path
from .views import checkin, mark_checkin, search_attendees_api

urlpatterns = [
    path('checkin/', checkin, name='checkin'),
    path('checkin/<int:id>/', mark_checkin, name='mark_checkin'),
    path('api/search/', search_attendees_api, name='search_api'),
]

