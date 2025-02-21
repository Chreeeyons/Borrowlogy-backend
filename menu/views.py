from django.shortcuts import render

# Create your views here.
def menu_view(request):
    return render(request, "ltmenupage.html")

def brwmenu_view(request):
    return render(request, "brwmenupage.html")