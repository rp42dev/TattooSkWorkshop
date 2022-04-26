from django.shortcuts import render, get_object_or_404
from .models import Album, Artist
from django.db.models import Q
from django.contrib import messages


def gallery(request):
    """A view to return the gallery page and show all album"""
    artists = Artist.objects.all()

    context = {
        'artists': artists,
    }

    return render(request, 'album/gallery.html', context)


def artist(request, artist_name):
    """A view to return the artist page and show all album"""
    
    album = Album.objects.filter(artist__name=artist_name)

    context = {
        'album': album,
        'artist': artist,
        'artist_name': artist_name
        }

    return render(request, 'album/artist.html', context)


def details(request, artist_name, item_id):
    """ A view to show individual image with details """

    item = get_object_or_404(Album, pk=item_id)
    album = Album.objects.filter(artist__name=artist_name)

    context = {
        'item_id': int(item_id),
        'item': item,
        'album': album,
        'artist_name': artist_name,
    }
    print()
    return render(request, 'album/details.html', context)

