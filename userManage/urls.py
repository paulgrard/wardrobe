from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('userManage.views',
    url(r'^add$', 'add', name='add'),
    #url(r'^delete$', 'delete', name='delete'),
)

