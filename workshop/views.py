from django.shortcuts import render, redirect
from django.conf import settings
from django.templatetags.static import static
from .models import About, AddMember, Faq


def workshop(request):
    """A view to return the workshop page and show all album"""
    allObjects = About.objects.all()
    
    context = {
        'index': 'about',
        'allObjects': allObjects,
    }
    
    if request.htmx:
        context['obj'] = allObjects.filter(name=request.GET['name'])
        print(context['obj'])
        return render(request, 'includes/carousel.html', context)

    return render(request, 'workshop/workshop.html', context)
    

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