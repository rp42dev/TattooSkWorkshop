from django.db import models
from django_resized import ResizedImageField
from embed_video.fields import EmbedVideoField
from django.urls import reverse



class Seo(models.Model):
    """ SEO model """
    title = models.CharField(max_length=200, blank=True)
    title_no = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=160, blank=True)
    description_no = models.TextField(max_length=160, blank=True)
    keywords = models.TextField(blank=True)
    keywords_no = models.TextField(blank=True)
    image = ResizedImageField(
        size=[1200, 630], quality=100, upload_to='seo', blank=True, null=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    """ Page model """
    name = models.CharField(max_length=200, blank=True)
    name_no = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_no = models.TextField(blank=True)
    seo = models.ForeignKey(
        'Seo', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse(self.slug)

    def __str__(self):
        return self.name

class Section(models.Model):
    """ Section model """
    title = models.CharField(max_length=200, blank=True)
    title_no = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    subtitle_no = models.CharField(max_length=300, blank=True)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.page.name
    

class Image(models.Model):
    """ Images model """
    ASPECT_RATIOS = [('original', 'Original'), ('landscape', 'Landscape 16x9'),
                     ('portrait', 'Portrait 9x16'), ('square', 'Square 1x1')]
    SIZES = {'original': [2560, 2560], 'landscape': [
        2560, 1440], 'portrait': [1440, 2560], 'square': [1440, 1440]}

    title = models.CharField(max_length=200, blank=True)
    title_no = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_no = models.TextField(blank=True)
    aspect_ratio = models.CharField(
        choices=ASPECT_RATIOS, max_length=20, default='Original')
    image = ResizedImageField(
        size=[2560, 2560], quality=100, upload_to='images/', blank=True, null=True)
    url = models.URLField(blank=True, null=True, default=None)
    pages = models.ManyToManyField('Page', blank=True)
    sections = models.ManyToManyField('Section', blank=True)
    articles = models.ManyToManyField('Article', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    """ Article model """
    title = models.CharField(max_length=200, blank=True)
    title_no = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    subtitle_no = models.CharField(max_length=200, blank=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(blank=True)
    body_no = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.section.title
    

class Element(models.Model):
    """ Article model """
    name = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    body_no = models.TextField(blank=True)
    pages = models.ManyToManyField('Page', blank=True)
    sections = models.ManyToManyField('Section', blank=True)
    articles = models.ManyToManyField('Article', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video model """
    title = models.CharField(max_length=200, blank=True)
    title_no = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_no = models.TextField(blank=True)
    video = EmbedVideoField(blank=True, null=True)
    pages = models.ManyToManyField('Page', blank=True)
    sections = models.ManyToManyField('Section', blank=True)
    articles = models.ManyToManyField('Article', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.section.title + ' - ' + self.article.title
