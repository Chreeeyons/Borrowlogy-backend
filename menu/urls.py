from django.urls import path
from .views import brw_equipments
from . import views
from .views import test_api

urlpatterns = [
    path('ltmenu', views.menu_view, name='menu_page'),
    # path('logout/', views.logout_view, name='logout'),
    # path('brwmenu/', views.brwmenu_view, name='brwmenu'),
    path('brwequipments/', brw_equipments, name='brw_equipments'),
    path("test/", test_api, name="test-api"),
]