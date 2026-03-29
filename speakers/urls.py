from django.urls import path
from .views import speaker_apply, speaker_success

urlpatterns = [
    path('speaker/apply/', speaker_apply, name='speaker_apply'),
    path('speaker/success/', speaker_success, name='speaker_success'),
]