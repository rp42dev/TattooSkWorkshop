from django.shortcuts import render, redirect
from django.conf import settings
from django.templatetags.static import static
from .models import About, AddMember, Faq

# Create your views here.


def workshop(request):
    """A view to return the workshop page and show all album"""
   
    andrej = About.objects.filter(name='andrej').order_by('order')
    diana = About.objects.filter(name='diana').order_by('order')
    jane = About.objects.filter(name='jane').order_by('order')
    shop = About.objects.filter(name='shop').order_by('order')

    context = {
        'shop': shop,
        'andrej': andrej,
        'jane': jane,
        'diana': diana,
    }

    return render(request, 'workshop/workshop.html', context)
    

def faq(request):
    """A view to return the faq page"""
    items = Faq.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'faq/faq.html', context)


def aftercare(request):
    """A view to return the faq page"""
    return render(request, 'aftercare/aftercare.html')


def map(request):
    """A view to return the map page"""
    return render(request, 'map/map.html')


def prices(request):
    """A view to return the map page"""
    return render(request, 'prices/prices.html')