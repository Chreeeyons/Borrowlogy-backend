from django.shortcuts import render

# Create your views here.
def menu_view(request):
    return render(request, "ltmenupage.html")

# def brwmenu_view(request):
#     return render(request, "brwequipment.html")

def brw_equipments(request):
    return render(request, 'brwequipment.html')