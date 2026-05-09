from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django_resized import ResizedImageField
from pillow_heif import register_heif_opener
from django.utils.translation import gettext_lazy as _

from home.models import Seo, Page
register_heif_opener()


from dproject.constants import ASPECT_RATIOS, SIZES


class Artist(models.Model):
    """Artist model"""
    name = models.CharField(max_length=254)
    image = ResizedImageField(
        size=[2560, 2560], quality=100,
        upload_to='artist', blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)
    slug_no = models.SlugField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("gallery", kwargs={"slug": self.slug})


    def get_friendly_name(self):
        return self.name  # Fixed: friendly_name field was missing

    def __str__(self):
        return self.name


class Album(models.Model):
    """Album model"""
    ASPECT_RATIOS = ASPECT_RATIOS
    SIZES = SIZES

    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    aspect_ratio = models.CharField(
        choices=ASPECT_RATIOS, max_length=20, default='original')
    image = ResizedImageField(
        size=[2560, 2560], quality=100, upload_to='album', blank=True, null=True)
    seo = models.ForeignKey(
        Seo, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)
    slug_no = models.SlugField(auto_created=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("details", kwargs={"artist_slug": self.artist.slug, "slug": self.slug})

    def __str__(self):
        return self.name
