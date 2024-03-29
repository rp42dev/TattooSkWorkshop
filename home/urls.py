from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    path('', views.index, name='home'),
    path('contact_form/', views.contact_form, name='contact_form'),
    path('send_mail/', views.send_email, name='send_mail'),
]
