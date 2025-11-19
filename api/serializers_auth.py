from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models_profile import Profile
from django.contrib.auth.password_validation import validate_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("role", "phone")

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "profile")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, required=False, default="client")
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "first_name", "last_name", "role", "phone")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop("role", "client")
        phone = validated_data.pop("phone", "")
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Profile will be created by signal, but set fields if needed
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.phone = phone
        profile.save()
        return user
