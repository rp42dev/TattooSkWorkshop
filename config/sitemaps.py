# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from album.models import Artist, Album


class ArtistSitemap(sitemaps.Sitemap):
    i18n = True
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Artist.objects.all()

    def location(self, artist):
        return reverse("artist", kwargs={"slug": artist.slug})


class ArtistItemSitemap(sitemaps.Sitemap):
    i18n = True
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Album.objects.all()

    def location(self, item):
        return reverse("details", kwargs={"slug": item.artist.slug, "item_id": item.id})


class StaticViewSitemap(sitemaps.Sitemap):
    i18n = True

    static_url_list = [
        {'url': 'home', 'priority': 0.4, 'changefreq': "monthly"},
        {'url': 'about', 'priority': 0.8, 'changefreq': "monthly"},
        {'url': 'faq', 'priority': 0.4, 'changefreq': "monthly"},
        {'url': 'aftercare', 'priority': 0.6, 'changefreq': "monthly"},
        {'url': 'prices', 'priority': 0.4, 'changefreq': "monthly"},
        {'url': 'gallery', 'priority': 0.5, 'changefreq': "monthly"},
    ]

    def items(self):
        return [item['url'] for item in self.static_url_list]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {element['url']: element['priority'] for element in self.static_url_list}[item]

    def changefreq(self, item):
        return {element['url']: element['changefreq'] for element in self.static_url_list}[item]


