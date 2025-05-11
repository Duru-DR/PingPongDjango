from rest_framework import serializers
from ..models import Profile

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'wins', 'loses',
        )
