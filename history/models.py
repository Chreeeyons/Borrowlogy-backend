from django.db import models
from django.conf import settings
from equipment.models import Equipment  # assuming you have an Equipment model

class TransactionHistory(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
    ])
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.borrower} - {self.equipment.name} - {self.status}"
