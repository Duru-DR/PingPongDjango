from rest_framework import serializers
from ..models       import Profile

class ProfileImageUploadSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ['picture']

    def validate_picture(self, value):
        max_size = 7 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Image size exceeds 7MB.")
        return value

class ProfileBackgroundUploadSerializer(serializers.ModelSerializer):
    background_picture = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ['background_picture']

    def validate_background_picture(self, value):
        max_size = 7 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Image size exceeds 7MB.")
        return value
        