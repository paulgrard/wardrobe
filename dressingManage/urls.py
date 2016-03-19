from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^$', views.accueil, name='accueil'),
    url(r'^addClothe$',views.addClothe, name='addClothe'),
    url(r'^editClothe/(?P<idC>\d+)$',views.editClothe, name='editClothe'),
    url(r'^getAllClothes$',views.getAllClothes, name='getAllClothes'),
    url(r'^getClothesFromCategory/(?P<idC>\d+)$', views.getClothesFromCategory, name='getClothesFromCategory'),
    url(r'^addTheme$',views.addTheme, name='addTheme'),
    url(r'^getThemes$',views.getThemes, name='getThemes'),
    url(r'^getTheme$',views.getTheme, name='getTheme'),
    url(r'^deleteTheme/(?P<idT>\d+)$', views.deleteTheme, name='deleteTheme'),
    url(r'^getColors/(?P<idC>\d+)$', views.getColors, name='getColors'),
    url(r'^getAllColors$', views.getAllColors, name='getAllColors'),
    url(r'^getPicture/(?P<idC>\d+)$', views.getPicture, name='getPicture'),
    url(r'^getWeather$', views.getWeather, name='getWeather'),
    url(r'^getCategoriesFromArea/(?P<idA>\d+)$', views.getCategoriesFromArea, name='getCategoriesFromArea'),
    url(r'^changeState/(?P<idC>\d+)/(?P<state>\d+)$', views.changeState, name='changeState'),
    url(r'^setGenerating/(?P<generatingState>\d+)$', views.setGenerating, name='setGenerating'),
    url(r'^generateOutfit/$', views.generateOutfit, name='generateOutfit'),
    url(r'^switchClothe/(?P<idC>\d+)/(?P<way>\d+)$', views.switchClothe, name='switchClothe'),
    url(r'^getOutfitSettings/$', views.getOutfitSettings, name='getOutfitSettings'),
]
