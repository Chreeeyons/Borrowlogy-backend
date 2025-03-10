from django.contrib import admin
from .models import Equipment

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')  

admin.site.register(Equipment, EquipmentAdmin)