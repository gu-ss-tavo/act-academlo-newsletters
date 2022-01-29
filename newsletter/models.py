from django.db import models

from user.models import CustomUser
from tag.models import Tag

# Create your models here.
class Newsletter(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)

    image = models.ImageField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    meta = models.BigIntegerField(default=0)
    votes = models.ManyToManyField(CustomUser, blank=True, related_name='votes')

    users = models.ManyToManyField(CustomUser, blank=True, related_name='users')
    tags = models.ManyToManyField(Tag, blank=True)
