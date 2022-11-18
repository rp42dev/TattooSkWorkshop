from django.contrib import admin
from .models import Album, Artist
from pyheif_pillow_opener import register_heif_opener

register_heif_opener()

# Register your models here.


class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'artist',
        'image',

    )


class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'order',
    )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)