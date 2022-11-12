from django.db import models
from django.conf import settings
import random
from django.db import models
from django_resized import ResizedImageField


class Artist(models.Model):
    name = models.CharField(max_length=254)
    image = ResizedImageField(size=[600, 900], crop=['middle', 'center'], quality=80, upload_to='artist')

    random_string = random.randint(1, 10)
    order = models.IntegerField(
        default=random_string,
        null=False, blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Album(models.Model):
    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    image = ResizedImageField(size=[800, 1200], crop=['middle', 'center'], quality=80, upload_to='album')

    def __str__(self):
        return self.name