from django.db import models
from django_resized import ResizedImageField
from album.models import Artist
from pillow_heif import register_heif_opener

register_heif_opener()

class Faq(models.Model):
    name = models.CharField(max_length=254, default='name')
    lang = models.CharField(max_length=2,  default='en')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name