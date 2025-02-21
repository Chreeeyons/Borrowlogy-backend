from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        print('here')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("menu_page")
    
    return render(request, "auth/login.html", {"form": form})

def brwlogin_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        print('here')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("menu_page")
    
    return render(request, "auth/brwlogin.html", {"form": form})

def homepage(request):
    return render(request, "homepage.html")  # Django will now find it in templates/