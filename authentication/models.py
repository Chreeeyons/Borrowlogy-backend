from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('lab_technician', 'Lab Technician'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]  # Set username from email
        super().save(*args, **kwargs)
