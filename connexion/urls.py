from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('connexion.views',
    url(r'^$', 'connexion', name='connexion'),
    #url(r'^deconnexion$', 'deconnexion', name='deconnexion'),
)

