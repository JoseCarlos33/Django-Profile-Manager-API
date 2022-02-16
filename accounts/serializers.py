from rest_framework import serializers

from accounts.models import UserProfile, ResearchedCities

class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    current_city = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchedCities
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'current_city')