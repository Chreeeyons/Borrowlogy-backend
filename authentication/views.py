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
        email = request.POST.get("username")  # Get the entered UP Mail
        user = authenticate(request, username=email)  # Use email instead of username

        if user:
            login(request, user)
            return redirect("menu_page")  # Redirect after successful login
        else:
            return render(request, "auth/brwlogin.html", {"error": "Invalid UP mail"})

    return render(request, "auth/brwlogin.html")

def homepage(request):
    return render(request, "homepage.html")  # Django will now find it in templates/


def logout_view(request):
    logout(request)
    return redirect('homepage')  # Redirect to homepage after logout

def forgot_password_view(request):
    return render(request, 'LTforgot-password.html')