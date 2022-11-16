from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<slug:slug>/', views.artist, name='artist'),
    path('<slug:slug>/<item_id>', views.details, name='details'),
]
