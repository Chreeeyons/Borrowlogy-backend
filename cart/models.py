from django.db import models
from django.conf import settings

class Material(models.Model):
    name = models.CharField(max_length=100)
    quantity_available = models.PositiveIntegerField(default=0)
    # other fields like description, category, etc.

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.material.name} x {self.quantity if self.material else 'N/A'}"
