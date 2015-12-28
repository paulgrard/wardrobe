from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('dressingManage.views',
    url(r'^$', 'accueil'),
    url(r'^addClothe$','addClothe'),
    url(r'^getAllClothes$','getAllClothes'),
)

