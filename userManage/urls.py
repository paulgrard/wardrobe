from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('userManage.views',
    url(r'^add$', 'add', name='add'),
    url(r'^deactivate$', 'deactivate', name='deactivate'),
)

