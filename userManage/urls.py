from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^add$', views.add, name='add'),
    url(r'^deactivate$', views.deactivate, name='deactivate'),
    url(r'^setParameters$', views.setParameters, name='setParameters'),
    url(r'^getParameters$', views.getParameters, name='getParameters'),
]
