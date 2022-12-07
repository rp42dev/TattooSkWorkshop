from django.views.generic import DetailView
from django.shortcuts import render
from django.conf import settings
from .models import Faq
from home.models import Page, Section, Article, Image, Video, Element


class PageDetailView(DetailView):
    """ A view to show individual image with details """
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context['section'] = Section.objects.get(
                title=self.request.GET['name'])
            context['articles'] = Article.objects.filter(
                section=context['section'])
            if Image.objects.filter(articles__in=context['articles']).exists():
                context['images'] = Image.objects.filter(
                    articles__in=context['articles'])
            elif Image.objects.filter(sections=context['section']).exists():
                context['images'] = Image.objects.filter(
                    sections=context['section'])
            return context
        else:
            context['sections'] = Section.objects.filter(page=self.object)
            return context

    def get_template_names(self):
        if self.request.htmx:
            return 'includes/about_items.html'
        else:
            return 'pages/about.html'
    
    

def faq(request):
    """A view to return the faq page"""
    items = Faq.objects.all()
    
    context = {
        'items': items,
        'index': 'faq',
    }
    
    return render(request, 'pages/faq.html', context)


def aftercare(request):
    """A view to return the faq page"""
    
    context = {
        'index': 'aftercare',
    }
    
    return render(request, 'pages/aftercare.html', context)


def map(request):
    """A view to return the map page"""
    
    context = {
        'index': 'map',
    }
    
    return render(request, 'pages/map.html', context)


def prices(request):
    """A view to return the map page"""
    
    context = {
        'index': 'prices',
    }
    
    return render(request, 'pages/prices.html', context)