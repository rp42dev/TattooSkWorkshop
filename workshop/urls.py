from django.urls import path
from . import views
from .views import PageDetailView

from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path(_(r'<slug:slug>'), PageDetailView.as_view(), name='page'),
    path(_(r'faq'), views.faq, name='faq'),
    path(_(r'aftercare'), views.aftercare, name='aftercare'),
    path(_(r'map'), views.map, name='map'),
    path(_(r'prices'), views.prices, name='prices'),
]
