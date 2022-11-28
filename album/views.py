from django.shortcuts import render, get_object_or_404
from .models import Album, Artist
from django.db.models import Q
from django.contrib import messages


def gallery(request):
    """A view to return the gallery page and show all album"""
    artists = Artist.objects.all().order_by('order')

    context = {
        'artists': artists,
        'index': 'gallery',
    }

    return render(request, 'album/gallery.html', context)


def artist(request, slug):
    """A view to return the artist page and show all album"""

    album = Album.objects.filter(artist__slug=slug)
    artist = get_object_or_404(Artist, slug=slug)
    context = {
        'album': album,
        'artist': artist,
        'index': 'gallery',
        }

    return render(request, 'album/artist.html', context)


def details(request, artist_slug, slug):
    """ A view to show individual image with details """
    item = get_object_or_404(Album, slug=slug)
    print(item)
    album = Album.objects.filter(artist__slug=artist_slug)
    
    context = {
        'item_id': int(item.id),
        'item': item,
        'album': album,
        'artist_slug': artist_slug,
        'index': 'gallery',
    }

    return render(request, 'album/details.html', context)

