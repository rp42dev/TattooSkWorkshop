from django.urls import path
from .views import ArtistView, GalleryView, AlbumDetailView


urlpatterns = [
    path('', ArtistView.as_view(), name='artist'),
    path('<slug:slug>/', GalleryView.as_view(), name='gallery'),
    path('<slug:artist_slug>/<slug:slug>',
         AlbumDetailView.as_view(), name='details'),
]
