from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^$', views.accueil),
    url(r'^addClothe$',views.addClothe),
    url(r'^getAllClothes$',views.getAllClothes),
    url(r'^createTheme$',views.createTheme),
]
