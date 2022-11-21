from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from . import views

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    path('', views.index, name='home'),
    path('send_email', views.send_email, name='send_email'),
]
