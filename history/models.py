from django.db import models
from django.conf import settings
from django.utils import timezone

class TransactionHistory(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)    
    status = models.CharField(max_length=20, choices=[
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ])
    remarks = models.TextField(blank=True)
    labtech_remarks = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.borrower}  - {self.status}"
