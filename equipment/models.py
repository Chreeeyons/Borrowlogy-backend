from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()  # Ensure this field exists

    def __str__(self):
        return self.name