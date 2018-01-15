# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from . import views
from asset.api import views as api_views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/server', api_views.ServerListView.as_view(), name='dd'),
    url(r'^api/user', api_views.UserListView.as_view(), name='dd'),
    url(r'^(?P<model_name>\w+)/(?P<id>\d+)/$', views.AssetDetail.as_view(), name='detail'),
    url(r'^(?P<model_name>\w+)/$', views.AssetList.as_view(), name='list'),
    url(r'^(?P<model_name>\w+)/edit/$', views.AssetUpdate.as_view(), name='edit'),
    url(r'^(?P<model_name>\w+)/add/$', views.AssetCreate.as_view(), name='add'),
    url(r'^(?P<model_name>\w+)/delete/(?P<pk>\d+)/$', views.AssetDelete.as_view(), name='delete'),
]