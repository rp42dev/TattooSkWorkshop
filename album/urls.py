from django.urls import path, re_path
from .views import ArtistView, GalleryView, AlbumDetailView
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    re_path('', ArtistView.as_view(), name='artist'),
    path('<slug:slug>/', GalleryView.as_view(), name='gallery'),
    path('<slug:artist_slug>/<slug:slug>', AlbumDetailView.as_view(), name='details'),
]
