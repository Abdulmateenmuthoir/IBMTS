from django.urls import path
from .views import sponsor_apply, sponsor_success

urlpatterns = [
    path('sponsor/apply/', sponsor_apply, name='sponsor_apply'),
    path('sponsor/success/', sponsor_success, name='sponsor_success'),
]