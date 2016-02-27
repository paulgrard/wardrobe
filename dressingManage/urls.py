from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^$', views.accueil),
    url(r'^addClothe$',views.addClothe),
    url(r'^editClothe/(?P<idC>\d+)$',views.editClothe),
    url(r'^getAllClothes$',views.getAllClothes),
    url(r'^getClothesFromCategory/(?P<idC>\d+)$', views.getClothesFromCategory),
    url(r'^addTheme$',views.addTheme),
    url(r'^getThemes$',views.getThemes),
    url(r'^getTheme$',views.getTheme),
    url(r'^deleteTheme/(?P<idT>\d+)$', views.deleteTheme),
    url(r'^getColors/(?P<idC>\d+)$', views.getColors),
    url(r'^getAllColors$', views.getAllColors),
    url(r'^getPicture/(?P<idC>\d+)$', views.getPicture),
    url(r'^getWeather$', views.getWeather),
]
