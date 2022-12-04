from django.contrib import admin
from .models import Album, Artist, Page, Seo
from pillow_heif import register_heif_opener

register_heif_opener()

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    
    list_display = (
        'name',
        'artist',
        'image',
    )
    search_fields = ('name', 'artist__name',)
    readonly_fields = ('created_at', 'updated_at', 'slug')

class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'order',
    )
    readonly_fields = ('slug', 'created_at', 'updated_at')
    list_display_links = ('name',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
