from django.urls import path
from . import views

from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', views.workshop, name='about'),
    path(_(r'faq'), views.faq, name='faq'),
    path(_(r'aftercare'), views.aftercare, name='aftercare'),
    path(_(r'map'), views.map, name='map'),
    path(_(r'prices'), views.prices, name='prices'),
]
