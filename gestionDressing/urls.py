from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('gestionDressing.views',
    url(r'^$', 'accueil'),
    #url(r'^$', 'connexion', name='connexion'),
    #url(r'^deconnexion$', 'deconnexion', name='deconnexion'),
)

