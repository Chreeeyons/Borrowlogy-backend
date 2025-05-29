from django.db import models

class Chemical(models.Model):
    chemical_name = models.CharField(max_length=100)
    mass = models.FloatField()  # Stored in grams (g)
    brand_name = models.CharField(max_length=100)
    is_hazardous = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('chemical_name', 'mass', 'brand_name')

    def __str__(self):
        return f"{self.chemical_name} ({self.mass}g) - {self.brand_name}"
