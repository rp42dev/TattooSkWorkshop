from django.urls import path, re_path
from .views import PageDetailView, AboutView

from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
]
