from django.db import models

class Chemical(models.Model):
    chemical_name = models.CharField(max_length=100)
    volume = models.FloatField()  # or DecimalField for more precision
    volume_unit = models.CharField(max_length=10, choices=[('mL', 'mL'), ('L', 'L')])
    brand_name = models.CharField(max_length=100)
    is_hazardous = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)  # ← Add this
    location = models.CharField(max_length=100, null=True, blank=True)  # ← Add this

    class Meta:
        unique_together = ('chemical_name', 'volume', 'volume_unit', 'brand_name')

    def __str__(self):
        return f"{self.chemical_name} ({self.volume}{self.volume_unit}) - {self.brand_name}"
