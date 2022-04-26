from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<artist_name>', views.artist, name='artist'),
    path('<artist_name>/<item_id>', views.details, name='details'),
]
