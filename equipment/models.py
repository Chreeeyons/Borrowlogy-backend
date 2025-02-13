from django.db import models

# Create your models here.

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.CharField(max_length=100)
    available = models.IntegerField()


    def __str__(self):
        return self.name