from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^$', views.accueil),
    url(r'^addClothe$',views.addClothe),
    url(r'^getAllClothes$',views.getAllClothes),
    url(r'^addTheme$',views.addTheme),
    url(r'^getThemes$',views.getThemes),
    url(r'^getTheme$',views.getTheme),
    url(r'^deleteTheme/(?P<id>\d+)$', views.deleteTheme),
]
