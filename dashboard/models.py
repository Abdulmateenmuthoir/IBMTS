from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    quote = models.TextField()
    photo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    display_on_site = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order', 'name')


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True)
    display_on_site = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'name')

    def __str__(self):
        return self.name
