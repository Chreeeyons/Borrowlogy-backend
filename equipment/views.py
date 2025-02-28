<<<<<<< HEAD
=======
# from django.shortcuts import render
# from .models import Equipment  # Ensure this matches your model name

# def brw_equipments(request):
#     equipments = Equipment.objects.all()  # Fetch all equipment data
#     return render(request, 'brwequipment.html', {'equipments': equipments})

>>>>>>> f187bfdd822db3fef1c0a0b27469db28648ea313
from django.shortcuts import render
from .models import Equipment  # Ensure this matches your model name

def brw_equipments(request):
    equipments = Equipment.objects.all()  # Fetch all equipment data
<<<<<<< HEAD
    return render(request, 'brwequipment.html', {'equipments': equipments})
=======
    
    for equipment in equipments:
        equipment.range = range(1, equipment.quantity + 1)  # Create a range for the dropdown

    return render(request, 'brwequipment.html', {'equipments': equipments})
>>>>>>> f187bfdd822db3fef1c0a0b27469db28648ea313
