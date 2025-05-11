from rest_framework import serializers
from ..models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'username', 'picture', 'rank', 'badge', 'background_picture'
        )
