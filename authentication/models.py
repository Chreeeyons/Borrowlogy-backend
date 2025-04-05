from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('borrower', 'Borrower'),
        ('lab_technician', 'Lab Technician'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='borrower')
    google_id = models.CharField(max_length=255, blank=True, null=True)  # For Google authentication
    
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]  # Set username from email
        super().save(*args, **kwargs)

