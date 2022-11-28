from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.db import models
from django.utils.timezone import now
import random


class Artist(models.Model):
    name = models.CharField(max_length=254)
    image = ResizedImageField(size=[600, 900], crop=['middle', 'center'], quality=80, upload_to='artist')
    slug = models.SlugField(blank=True, null=True)
    random_string = random.randint(1, 10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(
        default=random_string,
        null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/{self.slug}'

    def get_friendly_name(self):
        return self.friendly_name

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    image = ResizedImageField(size=[800, 1200], crop=['middle', 'center'], quality=80, upload_to='album')
    slug = models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return f'/{self.artist.slug}/{self.id}'
    
    def __str__(self):
        return self.name
