# from django.db import models
# from django.contrib.auth.models import User
# from django.apps import apps

# class Request(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Requesting user
#     equipment = models.ForeignKey('inventory.Equipment', on_delete=models.CASCADE)  # Use the app name where Equipment is defined
#     quantity = models.PositiveIntegerField()  # Requested quantity
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Request status
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for request creation
#     updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

#     def approve(self):
#         """Approve the request."""
#         self.status = 'approved'
#         self.save()

#     def reject(self):
#         """Reject the request."""
#         self.status = 'rejected'
#         self.save()

#     def __str__(self):
#         return f"{self.user.username} requested {self.quantity}x {self.equipment.name} ({self.status})"
