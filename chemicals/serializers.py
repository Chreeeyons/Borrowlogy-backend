from rest_framework import serializers
from .models import Chemical

class ChemicalSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display', read_only=True)

    class Meta:
        model = Chemical
        fields = [
            'id', 'chemical_name', 'mass', 'brand_name',
            'hazard_type', 'hazard_type_display', 'location', 'expiration_date'
        ]


    # # def validate(self, data):
    #     request = self.context.get('request')

    #     # Only allow lab techs to set/edit location and expiration_date
    #     if request and request.user.is_authenticated:
    #         if request.user.user_type != 'lab_tech':
    #             data.pop('location', None)
    #             data.pop('expiration_date', None)
    #     else:
    #         # If no user or anonymous, don't allow either field
    #         data.pop('location', None)
    #         data.pop('expiration_date', None)

    #     return data

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     request = self.context.get('request')

    #     # Hide location and expiration_date if user is not lab tech
    #     if not (request and request.user.is_authenticated and request.user.user_type == 'lab_tech'):
    #         rep.pop('location', None)
    #         rep.pop('expiration_date', None)
    #     return rep 