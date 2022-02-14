from rest_framework import serializers

from accounts.models import UserProfile

class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    current_city = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)

class SearchSerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=200)
    latitude = serializers.CharField(max_length=200)
    longitude = serializers.CharField(max_length=200)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'email', 'current_city')