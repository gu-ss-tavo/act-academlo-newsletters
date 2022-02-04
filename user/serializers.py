from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from newsletter.models import Newsletter

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = CustomUser(first_name=first_name, last_name=last_name, email=email, password=make_password(password))
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password',)

class NewsletterUsersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    delete_by_id = serializers.IntegerField(write_only=True, default=None)
    class Meta:
        model = Newsletter
        fields = ('id', 'name', 'description', 'delete_by_id')
