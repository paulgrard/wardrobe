from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('connection.views',
    url(r'^$', 'connection', name='connection'),
    url(r'^deconnection$', 'deconnection', name='deconnection'),
)

