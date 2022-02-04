from rest_framework import serializers

from .models import Newsletter

class NewsletterSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Newsletter
        fields = ('id', 'name', 'description', 'image', 'body', 'meta', 'vote_count', 'created_at')

class VoteNewsletterSerializer(serializers.Serializer):
    vote = serializers.CharField(max_length=6)

class UserNewsletterSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=False)
