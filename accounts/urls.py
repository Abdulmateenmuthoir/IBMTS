from django.urls import path
from .views import admin_login, admin_logout

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
]
