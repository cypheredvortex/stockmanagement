from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30)
    permissions = models.JSONField(default=dict)  # Permet de gérer des permissions spécifiques

    def __str__(self):
        return f"{self.user.username} - {self.role}"
