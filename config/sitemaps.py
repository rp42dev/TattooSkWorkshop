# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from album.models import Artist, Album
from datetime import datetime as dt


class ArtistSitemap(sitemaps.Sitemap):
    i18n=True

    def items(self):
        return Artist.objects.all()
    
    def location(self, artist):
        return reverse("artist", kwargs={"slug": artist.slug})
    
    def changefreq(self, item):
        return "monthly"


class ArtistItemSitemap(sitemaps.Sitemap):
    i18n = True

    def items(self):
        return Album.objects.all()

    def location(self, item):
        return reverse("details", kwargs={"slug": item.artist.slug, "item_id": item.id})
    
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