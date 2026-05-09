from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    path('', views.HomeView.as_view(), name='home'),
    path('contact_form/', views.ContactFormView.as_view(), name='contact_form'),
    path('send_mail/', views.ContactEmailView.as_view(), name='send_mail'),
]
