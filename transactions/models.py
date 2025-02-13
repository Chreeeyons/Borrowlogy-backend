from django.db import models
from equipment.models import Equipment

# Create your models here.

class Transaction(models.Model):

    # array? or dict with quantity. borrowed_equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    name_of_borrower = models.CharField(max_length=100)
    email_of_borrower = models.EmailField()
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    time_of_return = models.DateTimeField(null=True)
    returned = models.BooleanField(default=False)
    remarks = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.equipment} - {self.created_at}'