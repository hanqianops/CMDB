# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.AssetList.as_view(), name='asset_list'),
]