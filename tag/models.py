from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=50, unique='name')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
