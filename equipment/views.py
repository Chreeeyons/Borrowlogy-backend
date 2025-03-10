# from django.shortcuts import render
# from .models import Equipment  # Ensure this matches your model name

# def brw_equipments(request):
#     equipments = Equipment.objects.all()  # Fetch all equipment data
#     return render(request, 'brwequipment.html', {'equipments': equipments})

from django.shortcuts import render
from .models import Equipment  # Ensure this matches your model name

def brw_equipments(request):
    equipments = Equipment.objects.all()  # Fetch all equipment data
    return render(request, 'brwequipment.html', {'equipments': equipments})
