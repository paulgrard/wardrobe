from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.connection, name='connection'),
    url(r'^deconnection$', views.deconnection, name='deconnection'),
]
