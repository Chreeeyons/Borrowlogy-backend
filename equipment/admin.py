from django.contrib import admin
from django.apps import AppConfig

class EquipmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipment'  # This must match what you put in `INSTALLED_APPS`

# Register your models here.