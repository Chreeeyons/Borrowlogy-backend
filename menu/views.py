from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"message": "API is working!"})
@api_view(['GET'])

# Create your views here.
def menu_view(request):
    return render(request, "ltmenupage.html")

# def brwmenu_view(request):
#     return render(request, "brwequipment.html")

def brw_equipments(request):
    return render(request, 'brwequipment.html')