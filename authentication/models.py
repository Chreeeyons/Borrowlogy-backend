from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('borrower', 'Borrower'),
        ('lab_technician', 'Lab Technician'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='borrower')
    google_id = models.CharField(max_length=255, blank=True, null=True)  # For Google authentication
    name = models.CharField(max_length=255, blank=True, null=True)  # For storing the user's name
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(max_length=150, unique=True, blank=True)  # Optional username field

    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]  # Set username from email
        super().save(*args, **kwargs)

