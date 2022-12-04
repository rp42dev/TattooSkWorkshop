from django.contrib import admin
from .models import Page, Seo
from pillow_heif import register_heif_opener

register_heif_opener()

class PageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'description',
    )
    readonly_fields = ('created_at', 'updated_at', 'slug')


class SeoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'keywords',
        'image',
    )

    
admin.site.register(Seo, SeoAdmin)
admin.site.register(Page, PageAdmin)


