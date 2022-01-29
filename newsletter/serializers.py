from rest_framework import serializers

from .models import Newsletter

from user.serializers import CustomUserSerializer

class NewsletterSerializer(serializers.ModelSerializer):
    votes = CustomUserSerializer(read_only=True, many=True)
    class Meta:
        model = Newsletter
        fields = ('id', 'name', 'description', 'image', 'body', 'meta', 'votes', 'created_at')

class VoteNewsletterSerializer(serializers.Serializer):
    vote = serializers.CharField(max_length=6)

class UserNewsletterSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=False)
