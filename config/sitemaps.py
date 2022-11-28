# sitemaps.py
from django.contrib import sitemaps
from album.models import Artist, Album
from datetime import datetime as dt
from django.urls import reverse

class ArtistSitemap(sitemaps.Sitemap):
    i18n=True
    alternates = True
    x_default = 'no'

    def items(self):
        return Artist.objects.all()
    
    def lastmod(self, item):
        return item.updated_at


class ArtistItemSitemap(sitemaps.Sitemap):
    i18n = True
    alternates = True
    x_default = 'no'

    def items(self):
        return Album.objects.all()

    def lastmod(self, item):
        return item.updated_at

class StaticViewSitemap(sitemaps.Sitemap):
    i18n = True
    alternates = True
    x_default = 'no'
    
    static_url_list = [
        {'url': 'home'},
        {'url': 'about'},
        {'url': 'faq'},
        {'url': 'aftercare'},
        {'url': 'prices'},
        {'url': 'gallery'},
    ]

    def items(self):
        return [item['url'] for item in self.static_url_list]

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return dt.now()