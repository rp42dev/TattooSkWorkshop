from modeltranslation.translator import register, TranslationOptions
from .models import Seo, Page, Section, Faq, Image, Article, Element, Video

@register(Seo)
class SeoTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords')

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug')

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')

@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'body')

@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ('body',)

@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
