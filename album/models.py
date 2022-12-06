from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django_resized import ResizedImageField

from home.models import Seo, Page


class Artist(models.Model):
    """Artist model"""
    name = models.CharField(max_length=254)
    image = ResizedImageField(
        size=[2560, 2560], quality=100,
        upload_to='artist', blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    Page = models.ForeignKey(
        Page, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("gallery", kwargs={"slug": self.slug})

    def get_friendly_name(self):
        return self.friendly_name

    def __str__(self):
        return self.name


class Album(models.Model):
    """Album model"""
    ASPECT_RATIOS = [('original', 'Original'), ('landscape', 'Landscape 16x9'),
                     ('portrait', 'Portrait 9x16'), ('square', 'Square 1x1')]
    SIZES = {'original': [2560, 2560], 'landscape': [
        2560, 1440], 'portrait': [1440, 2560], 'square': [1440, 1440]}

    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    aspect_ratio = models.CharField(
        choices=ASPECT_RATIOS, max_length=20, default='Original')
    image = ResizedImageField(
        size=[2560, 2560], quality=100, upload_to='album', blank=True, null=True)
    seo = models.ForeignKey(
        Seo, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("details", kwargs={"artist_slug": self.artist.slug, "slug": self.slug})

    def __str__(self):
        return self.name
