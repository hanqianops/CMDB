# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from fortress import views
urlpatterns = [
    url(r'^loginhost/$', views.login_host, name='loginhost'),
    url(r'^menu/(?P<user>\w+)/$', views.menu, name='menu'),
    ]