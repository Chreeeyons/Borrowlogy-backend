from django.urls import path
from . import views

urlpatterns = [
    path('ltmenu', views.menu_view, name='menu_page'),
    # path('logout/', views.logout_view, name='logout'),
    path('brwmenu/', views.brwmenu_view, name='brwmenu'),
]