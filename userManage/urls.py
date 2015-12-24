from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('add.views',
    url(r'^add$', 'add', name='add'),
    url(r'^delete$', 'delete', name='delete'),
)

