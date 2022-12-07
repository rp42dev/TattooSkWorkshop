from django.contrib import admin
from .models import Page, Seo, Section, Article, Image, Video, Image, Element
from pillow_heif import register_heif_opener

register_heif_opener()


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class ImagePageInline(admin.TabularInline):
    model = Image.pages.through
    extra = 0


class ImageArticleInline(admin.TabularInline):
    model = Image.articles.through
    extra = 0


class ImageSectionInline(admin.TabularInline):
    model = Image.sections.through
    extra = 0


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


class ElementInline(admin.TabularInline):
    model = Element
    extra: 0

    inlines = [ImageInline]


class ElementPageInline(admin.TabularInline):
    model = Element.pages.through
    extra: 0

    inlines = [ImageInline]


class ElementSectionInline(admin.TabularInline):
    model = Element.sections.through
    extra: 0

    inlines = [ImageInline]


class ElementArticleInline(admin.TabularInline):
    model = Element.articles.through
    extra: 0

    inlines = [ImageInline]


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0

    inlines = [VideoInline, ImageArticleInline, ElementInline]


class VideoArticleInline(admin.TabularInline):
    model = Video.articles.through
    extra = 0


class VideoSectionInline(admin.TabularInline):
    model = Video.sections.through
    extra = 0


class VideoPageInline(admin.TabularInline):
    model = Video.pages.through
    extra = 0


class SectionInline(admin.TabularInline):
    model = Section
    extra: 0

    inlines = [ArticleInline, ImageSectionInline, ElementSectionInline]
    exclude = ('title_no', 'subtitle_no', 'description_no')


class PageInline(admin.TabularInline):
    model = Page
    extra: 0
    inlines = [SectionInline, ImagePageInline, ElementPageInline]


class SeoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )

    search_fields = ('title', 'description',)


class ElementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = ('name',)


class PageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )

    inlines = [SectionInline, ImagePageInline, ElementPageInline]
    readonly_fields = ('created_at', 'updated_at', 'slug')
    search_fields = ('name', 'slug')


class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'page',
    )

    inlines = [ArticleInline, ImageSectionInline, ElementSectionInline]

    list_select_related = ('page',)
    list_display_links = ('title', 'page')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'page__name')


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'image',
    )

    inlines = [ImagePageInline, ImageSectionInline, ImageArticleInline]
    list_display_links = ('title', 'image')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'image')


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'section',
    )

    inlines = [ImageArticleInline, ElementArticleInline, VideoArticleInline]
    list_select_related = ('section', 'section__page')
    list_display_links = ('title', 'section')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'section__title', 'section__page__name')


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    list_select_related = ('article',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Seo, SeoAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Video, VideoAdmin)
