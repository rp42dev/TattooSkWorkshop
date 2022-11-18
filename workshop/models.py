from django.db import models
from django_resized import ResizedImageField
from album.models import Artist
import random
from pillow_heif import register_heif_opener

register_heif_opener()

class AddMember(models.Model):

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class About(models.Model):
    
    random_string = random.randint(111, 999)
    member = models.ForeignKey(
        AddMember, null=True,
        blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    order = models.IntegerField(
        default=random_string,
        null=False, blank=False)
    image = ResizedImageField(size=[1200, 800], quality=100, crop=['middle', 'center'], upload_to='about')

    def __str__(self):
        return self.name


class Faq(models.Model):
    name = models.CharField(max_length=254, default='name')
    lang = models.CharField(max_length=2,  default='en')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name