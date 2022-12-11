from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Album, Artist, Page


class ArtistView(ListView):
    """A view to return the gallery page and show all album"""
    ordering = ['order']
    model = Artist
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='gallery')
        context['url'] = self.request.path
        
        
        return context


class GalleryView(ListView):
    """A view to return the artist page and show all album"""
    model = Album
    paginate_by: int = 8

    def get_queryset(self):
        self.artist = get_object_or_404(Artist, slug=self.kwargs['slug'])
        return Album.objects.filter(artist=self.artist).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.path
        context['artist'] = self.artist.name
        return context

    def get_template_names(self):
        if self.request.htmx:
            return 'includes/album_list_items.html'
        else:
            return 'album/album_list.html'


class AlbumDetailView(DetailView):
    """ A view to show individual image with details """
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev'] = Album.objects.filter(
            artist=self.object.artist, id__gt=self.object.id).first()
        context['next'] = Album.objects.filter(
            artist=self.object.artist, id__lt=self.object.id).last()
        return context

    def get_template_names(self):
        if self.request.htmx:
            return 'includes/album_detail_item.html'
        else:
            return 'album/album_detail.html'
