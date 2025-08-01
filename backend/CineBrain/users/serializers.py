# VanLifeApp/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
class RegisterUserSerializer(serializers.ModelSerializer):
    """the password field in the User model is not part of the default fields included by DRF
        By explicitly declaring it, you're telling DRF how to handle the password field.
    """
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
