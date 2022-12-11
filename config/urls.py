from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.utils.translation import gettext_lazy as _


from .sitemaps import StaticViewSitemap, ArtistSitemap, ArtistItemSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'artist': ArtistSitemap,
    'items': ArtistItemSitemap
}


urlpatterns = [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path(_('gallery/'), include('album.urls')),
    path(_('about/'), include('about.urls')),
    prefix_default_language=False
)
