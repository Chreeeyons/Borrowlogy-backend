from django.db import models

class Chemical(models.Model):
    HAZARD_TYPE_CHOICES = [
        ('No GHS', 'No GHS'),
        ('Flammable', 'Flammable'),
        ('Harmful', 'Harmful'),
        ('Health Hazard', 'Health Hazard'),
        ('Acute Toxicity', 'Acute Toxicity'),
        ('Environmental Hazard', 'Environmental Hazard'),
    ]

    chemical_name = models.CharField(max_length=100)
    mass = models.FloatField()  # Stored in grams (g)
    brand_name = models.CharField(max_length=100)
    hazard_type = models.CharField(
        max_length=20,
        choices=HAZARD_TYPE_CHOICES,
        default='No GHS'
    )
    expiration_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('chemical_name', 'mass', 'brand_name')

    def __str__(self):
        return f"{self.chemical_name} ({self.mass}g) - {self.brand_name}"
