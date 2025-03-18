from django.urls import path
from .views import brw_equipments
from .views import ltmenu

urlpatterns = [
    path('brwequipments/', brw_equipments, name='brw_equipments'),
    path('menu/ltmenu', ltmenu, name='ltmenu'),
]