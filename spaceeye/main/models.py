from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    FAVORITE_TYPES = [
        ('apod', 'NASA APOD'),
        ('mars_rover', 'Mars Rover Photo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite_type = models.CharField(max_length=20, choices=FAVORITE_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField()
    api_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'favorite_type', 'image_url']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"