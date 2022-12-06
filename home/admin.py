from django.contrib import admin
from .models import Page, Seo, Section, Article, ArticleImage, ArticleVideo
from pillow_heif import register_heif_opener

register_heif_opener()


class SeoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )
    
    search_fields = ('title', 'description',)

class PageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    
    readonly_fields = ('created_at', 'updated_at', 'slug')
    search_fields = ('name', 'slug')


class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'page',
    )

    list_select_related = ('page',)
    list_display_links = ('title', 'page')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'page__name')

class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'section',
    )
    
    list_select_related = ('section', 'section__page')
    list_display_links = ('title', 'section')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'section__title', 'section__page__name')
    
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'article',
        'section',
    )
    
    list_select_related = ('article', 'article__section', 'article__section__page')
    list_display_links = ('title', 'article', 'section')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'article__title', 'article__section__title', 'article__section__page__name')
        
        
class ArticleVideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'article',
        'section',
    )
    
    list_select_related = ('article', 'article__section', 'article__section__page')
    list_display_links = ('title', 'article', 'section')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'article__title', 'article__section__title', 'article__section__page__name') 
        

admin.site.register(Seo, SeoAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(ArticleVideo, ArticleVideoAdmin)


