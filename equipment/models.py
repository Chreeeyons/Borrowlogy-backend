# from django.db import models

# class Equipment(models.Model):
#     name = models.CharField(max_length=255)
#     quantity = models.IntegerField(default=0)
#     status = models.CharField(max_length=50, default="Available")  # Make sure this exists

#     def __str__(self):
#         return self.name


from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()  # Ensure this field exists

    def __str__(self):
        return self.name