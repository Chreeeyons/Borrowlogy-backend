from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User  # Import Django's built-in User model

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("menu_page")
        else:
            # Add error messages
            error_message = "Invalid Email Address or Password"
            return render(request, "auth/login.html", {"form": form, "error_message": error_message})

    return render(request, "auth/login.html", {"form": form})

def brwlogin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  # Ensure you collect passwords

        if not username.endswith("@up.edu.ph"):
            messages.error(request, "Only UP Mail accounts are allowed.")
            return render(request, "auth/brwlogin.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("brw_equipments")  # Redirect after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, "auth/brwlogin.html")

def homepage(request):
    return render(request, "homepage.html")  # Django will now find it in templates/


def logout_view(request):
    logout(request)
    return redirect('homepage')  # Redirect to homepage after logout

def forgot_password_view(request):
    return render(request, 'LTforgot-password.html')