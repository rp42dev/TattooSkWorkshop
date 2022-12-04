from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.dispatch import receiver
from PIL import Image
import os

class Seo(models.Model):
    """ SEO model """
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=160, blank=True)
    keywords = models.TextField(blank=True)
    image = models.ImageField(upload_to='seo/', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'

class Page(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    seo = models.ForeignKey(
        Seo, on_delete=models.CASCADE, blank=True, null=True)
    image = ResizedImageField(
        size=[2500, 1600], quality=100, upload_to='pages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        existing_name = Page.objects.filter(name=self.name)
        if existing_name:
            counter = 1
            while True:
                if not Page.objects.filter(
                        slug=slugify(self.name) + '-' + str(counter)).exists():
                    self.slug = slugify(self.name) + '-' + str(counter)
                    break
                counter += 1
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(models.signals.pre_save, sender=Page)
@receiver(models.signals.pre_save, sender=Seo)
def auto_delete_file_on_update(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is updated.
    """
    if not instance.pk:
        return False

    if not instance.image:
        return False

    if sender == Seo:
        try:
            old_file = Seo.objects.get(pk=instance.pk).image
        except Seo.DoesNotExist:
            return False
    elif sender == Page:
        try:
            old_file = Page.objects.get(pk=instance.pk).image
        except Page.DoesNotExist:
            return False

    new_file = instance.image
    try:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        pass


@receiver(models.signals.post_save, sender=Page)
def auto_check_file_size(sender, instance, **kwargs):
    """
    Checks file size and compresses if necessary
    """
    if not instance.pk:
        return False

    if not instance.image:
        return False

    if instance.image.size > 1000000:
        print("Image size too large")
        print(instance.image.size)
        image = Image.open(instance.image)
        image.save(instance.image.path, quality=80, optimize=True)
        print(instance.image.size)
    else:
        return False
