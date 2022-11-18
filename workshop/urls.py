from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.workshop, name='about'),
    path('faq', views.faq, name='faq'),
    path('aftercare', views.aftercare, name='aftercare'),
    path('map', views.map, name='map'),
    path('prices', views.prices, name='prices'),
]
