from django.contrib.auth    import get_user_model
from rest_framework         import serializers
from ..models               import CustomUser
from prfl.models            import Profile
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_2fa_enabled',
            'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at', 'updated_at'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
            
        Profile.objects.create(
            user=user,
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user
