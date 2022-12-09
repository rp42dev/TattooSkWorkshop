from django.urls import path
from . import views
from .views import PageDetailView

from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path(_(r'<slug:slug>/'), PageDetailView.as_view(), name='page'),
]
