from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from PIL import Image, ImageOps
import os

from home.models import Page, Image
from album.models import Artist, Album


@receiver(pre_save, sender=Page)
@receiver(pre_save, sender=Album)
@receiver(pre_save, sender=Artist)
def slugify_name(sender, instance, **kwargs):
    """Slugify name before saving"""
    if instance.slug:
        return
    instance.slug = slugify(instance.name)

    def get_next_slug():
        slug = slugify(instance.name)
        next_slug = slug
        num = 1
        while sender.objects.filter(slug=next_slug).exists():
            next_slug = f"{slug}-{num}"
            num += 1
        return next_slug

    instance.slug = get_next_slug()


@receiver(pre_save, sender=Album)
@receiver(pre_save, sender=Artist)
@receiver(post_save, sender=Image)
def delete_old_file_on_update(sender, instance, **kwargs):
    """Deletes file from filesystem"""
    if not instance.pk:
        return False

    if not instance.image:
        return False

    try:
        old_file = Album.objects.get(pk=instance.pk).image
        new_file = instance.image
        if old_file == new_file:
            return False
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    except Album.DoesNotExist:
        return False


@receiver(post_save, sender=Album)
@receiver(post_save, sender=Artist)
@receiver(post_save, sender=Image)
def pre_save_crop_images(sender, instance, **kwargs):
    """Crops images to aspect ratio"""
    if not instance.pk:
        return False

    if not instance.image:
        return False

    try:
        aspect_ratio = instance.aspect_ratio
    except AttributeError:
        return False

    if aspect_ratio == 'original':
        return False

    try:
        image = Image.open(instance.image)
        image = ImageOps.fit(
            image, instance.SIZES[aspect_ratio], method=0, bleed=0.0, centering=(0.5, 0.5))
        image = image.resize(
            (instance.SIZES[aspect_ratio][0], instance.SIZES[aspect_ratio][1]), Image.ANTIALIAS)
    except:
        return False

    image.save(instance.image.path)


@receiver(post_save, sender=Album)
@receiver(post_save, sender=Artist)
@receiver(post_save, sender=Image)
def image_post_save(sender, instance, **kwargs):
    """Checks file size and compresses if over 1MB"""
    if not instance.pk:
        return False

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
