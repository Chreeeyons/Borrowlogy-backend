from django.urls import path
from . import views
from .views import homepage



urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('lblogin/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('brwlogin/', views.brwlogin_view, name='brwlogin'),
    path("homepage", views.homepage, name="homepage"),
]