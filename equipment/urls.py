# from django.urls import path
# from .views import brw_equipments

# urlpatterns = [
#     path('brwequipments/', brw_equipments, name='brw_equipments'),
# ]


from django.urls import path
from .views import brw_equipments

urlpatterns = [
    path('brwequipments/', brw_equipments, name='brw_equipments'),
]