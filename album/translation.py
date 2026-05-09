from modeltranslation.translator import register, TranslationOptions
from .models import Artist, Album

@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = ('slug',) # Artist name is usually not translated, but slug might be.

@register(Album)
class AlbumTranslationOptions(TranslationOptions):
    fields = ('slug',)
