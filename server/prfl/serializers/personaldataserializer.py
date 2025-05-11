from rest_framework import serializers
from ..models import Profile

class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'picture', 'background_picture', 'username', 'email', 'first_name', 'last_name'
            , 'country', 'city', 'address', 'zip_code'
        )
