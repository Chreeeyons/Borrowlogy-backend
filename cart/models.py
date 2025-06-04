from django.db import models
from django.conf import settings
from equipment.models import Equipment  # Assuming you have an Equipment model
from history.models import TransactionHistory  # Assuming you have a TransactionHistory model
from chemicals.models import Chemical

class Material(models.Model):
    name = models.CharField(max_length=100)
    quantity_available = models.PositiveIntegerField(default=0)
    # other fields like description, category, etc.

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TransactionHistory = models.ForeignKey(TransactionHistory, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
    chemicals = models.ForeignKey(Chemical, on_delete=models.CASCADE, null=True, blank=True)  # Link to Material model
    quantity = models.PositiveIntegerField()
    approved = models.BooleanField(default=False)  # Indicates if the item is approved
    return_quantity = models.PositiveIntegerField(default=0)  # Quantity to be returned
    return_date = models.DateField(null=True, blank=True)  # Indicates if the item is returned

    class Meta:
        unique_together = ('cart', 'equipment')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.equipment.name} {self.quantity if self.equipment else 'N/A'}"

