import json
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import ApprovedGoogleUser

User = get_user_model()

def is_approved_google_user(email):
    return email.endswith("@up.edu.ph") and ApprovedGoogleUser.objects.filter(email=email).exists()

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email")
            name = data.get("name")
            google_id = data.get("google_id")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            if not is_approved_google_user(email):
                return JsonResponse({"error": "Unauthorized: Not an approved UP user"}, status=403)

            # Get or create user
            user, _ = User.objects.get_or_create(email=email, defaults={
                "name": name,
                "google_id": google_id,
                "user_type": "lab_technician",  # Or "borrower" if you want to separate roles
                "username": email.split("@")[0],
            })

            login(request, user)

            return JsonResponse({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "user_type": user.user_type,
                }
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
