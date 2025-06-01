from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name