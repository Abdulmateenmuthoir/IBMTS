from django.db import models

class Speaker(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    topic = models.CharField(max_length=255)
    bio = models.TextField()

    linkedin = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    display_on_site = models.BooleanField(default=False)
    display_title = models.CharField(max_length=255, blank=True, help_text='Role or session title shown on the website')
    photo_url = models.URLField(blank=True, help_text='Public image URL shown on the website')
    image = models.ImageField(upload_to='speakers/', blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order', 'name')
