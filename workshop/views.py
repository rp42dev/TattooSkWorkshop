from django.shortcuts import render, redirect
from django.conf import settings
from django.templatetags.static import static
from .models import About, AddMember, Faq
from home.models import Page, Section, Article, ArticleImage, ArticleVideo


def about(request):
    """A view to return the about page and show all album"""
    page = Page.objects.get(name='about')
    sections = Section.objects.filter(page=page)

    context = {
        'page': page,
        'sections': sections,
    }
    
    if request.htmx:
        context['section'] = Section.objects.get(title=request.GET['name'])
        context['articles'] = Article.objects.filter(section=context['section'])
        context['images'] = ArticleImage.objects.filter(article__in=context['articles'])
        return render(request, 'includes/about_items.html', context)

    return render(request, 'about/about.html', context)
    

def faq(request):
    """A view to return the faq page"""
    items = Faq.objects.all()
    
    context = {
        'items': items,
        'index': 'faq',
    }
    
    return render(request, 'faq/faq.html', context)


def aftercare(request):
    """A view to return the faq page"""
    
    context = {
        'index': 'aftercare',
    }
    
    return render(request, 'aftercare/aftercare.html', context)


def map(request):
    """A view to return the map page"""
    
    context = {
        'index': 'map',
    }
    
    return render(request, 'map/map.html', context)


def prices(request):
    """A view to return the map page"""
    
    context = {
        'index': 'prices',
    }
    
    return render(request, 'prices/prices.html', context)