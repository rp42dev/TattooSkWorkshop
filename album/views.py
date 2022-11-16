from django.shortcuts import render, get_object_or_404
from .models import Album, Artist
from django.db.models import Q
from django.contrib import messages


def gallery(request):
    """A view to return the gallery page and show all album"""
    artists = Artist.objects.all().order_by('order')

    context = {
        'artists': artists,
    }

    return render(request, 'album/gallery.html', context)


def artist(request, slug):
    """A view to return the artist page and show all album"""

    album = Album.objects.filter(artist__slug=slug)

    context = {
        'album': album,
        'artist': artist,
        'artist_name': slug
        }

    return render(request, 'album/artist.html', context)


def details(request, slug, item_id):
    """ A view to show individual image with details """
    item = get_object_or_404(Album, pk=item_id)
    album = Album.objects.filter(artist__slug=slug)

    context = {
        'item_id': int(item_id),
        'item': item,
        'album': album,
        'artist_name': slug,
    }
    print()
    return render(request, 'album/details.html', context)

