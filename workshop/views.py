from django.views.generic import DetailView
from django.shortcuts import render
from django.conf import settings
from .models import Faq
from home.models import Page, Section, Article, Image, Video, Element
from django.utils.translation import gettext_lazy as _
from django.utils.translation import to_locale, get_language


class PageDetailView(DetailView):
    """ A view to show individual image with details """
    model = Page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context['section'] = Section.objects.get(
                id=self.request.GET['name'])
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
            print(self.object.name)
            return context

    def get_template_names(self):
        page_name = self.object.name
        if self.request.htmx:
            return f"includes/{page_name}_items.html"
        return 'pages/about.html'


def faq(request):
    """A view to return the faq page"""
    items = Faq.objects.all()
    
    context = {
        'items': items,
        'index': 'faq',
    }
    
    return render(request, 'pages/faq.html', context)


def map(request):
    """A view to return the map page"""
    
    context = {
        'index': 'map',
    }
    
    return render(request, 'pages/map.html', context)
