from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    # username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"   
