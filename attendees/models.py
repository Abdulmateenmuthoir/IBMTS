
# attendees/models.py

from django.db import models

class Attendee(models.Model):
    CATEGORY_CHOICES = [
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('entrepreneur', 'Entrepreneur'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name