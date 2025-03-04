from django.shortcuts import render
from .models import Equipment  # Ensure this matches your model name

def brw_equipments(request):
    equipments = Equipment.objects.all()  # Fetch all equipment data
    
    for equipment in equipments:
        equipment.range = range(1, equipment.quantity + 1)  # Create a range for the dropdown

    return render(request, 'brwequipment.html', {'equipments': equipments})
