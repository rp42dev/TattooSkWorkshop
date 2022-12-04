from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.utils.timezone import now
from PIL import Image
import os
from home.models import Seo, Page


class Artist(models.Model):
    """
    Artist model
    Includes following fields:
    - name
    - image
    - slug
    - created_at
    - updated_at
    - description
    - slogan
    - order
    - Seo -(foreign key)
    - Page -(foreign key)
    Includes following methods:
    - save
    - get_absolute_url
    - get_friendly_name
    - __str__ name
    """
    name = models.CharField(max_length=254)
    image = ResizedImageField(
        size=[2500, 2500], quality=100,
        upload_to='artist', blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    Page = models.ForeignKey(
        Page, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        existing_name = Artist.objects.filter(name=self.name)
        if existing_name:
            counter = 1
            while True:
                if not Artist.objects.filter(
                        slug=slugify(self.name) + '-' + str(counter)).exists():
                    self.slug = slugify(self.name) + '-' + str(counter)
                    break
                counter += 1
        super(Artist, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery", kwargs={"slug": self.slug})

    def get_friendly_name(self):
        return self.friendly_name

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Album model

    Includes the following fields:
    - name
    - artist -(foreign key)
    - image
    - seo -(foreign key)
    - page -(foreign key)
    - slug
    - created_at
    - updated_at
    Includes the following methods:
    - save
    - get_absolute_url
    - __str__
    """
    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    image = ResizedImageField(
        size=[2500, 2500], quality=100, upload_to='album', blank=True, null=True)
    seo = models.ForeignKey(
        Seo, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        existing_name = Album.objects.filter(name=self.name)
        if existing_name:
            counter = 1
            while True:
                if not Album.objects.filter(
                        slug=slugify(self.name) + '-' + str(counter)).exists():
                    self.slug = slugify(self.name) + '-' + str(counter)
                    break
                counter += 1
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("details", kwargs={"artist_slug": self.artist.slug, "slug": self.slug})

    def __str__(self):
        return self.name


@receiver(models.signals.pre_save, sender=Page)
@receiver(models.signals.pre_save, sender=Album)
@receiver(models.signals.pre_save, sender=Artist)
def auto_delete_file_on_update(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is updated.
    """
    if not instance.pk:
        return False

    if not instance.image:
        return False

    if sender == Album:
        try:
            old_file = Album.objects.get(pk=instance.pk).image
        except Album.DoesNotExist:
            return False
    elif sender == Artist:
        try:
            old_file = Artist.objects.get(pk=instance.pk).image
        except Artist.DoesNotExist:
            return False

    new_file = instance.image
    try:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        pass


@receiver(models.signals.post_save, sender=Page)
@receiver(models.signals.post_save, sender=Album)
@receiver(models.signals.post_save, sender=Artist)
def auto_check_file_size(sender, instance, **kwargs):
    """
    Checks file size and compresses if necessary
    """
    if not instance.pk:
        return
    if not instance.image:
        return False
    try:
        if instance.image.size > 1000000:
            print("Image size too large")
            print(instance.image.size)
            image = Image.open(instance.image)
            image.save(instance.image.path, quality=80, optimize=True)
            print(instance.image.size)
    except:
        pass
