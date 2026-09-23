"""Recommendation models for Spotify-based music suggestions."""

from django.db import models
from users.models import UserProfile

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recommendations")
    tracks = models.JSONField(default=list)
    spotify_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return a readable label for this recommendation record."""
        return f"Recommendation for {self.user.email} - {self.created_at}"