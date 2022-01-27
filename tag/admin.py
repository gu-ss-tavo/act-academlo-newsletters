from django.contrib import admin

from tag.models import Tag

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
