
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

    # A registration is valid only after Paystack verifies the transaction.
    is_paid = models.BooleanField(default=False)
    ticket_amount = models.PositiveIntegerField(default=0, help_text='Amount in naira')
    payment_reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_transaction_id = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    registration_email_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
