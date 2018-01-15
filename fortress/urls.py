# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from fortress import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    url(r'^terminal/$', views.terminal, name='terminal'),
    url(r'^close/$', csrf_exempt(views.CloseTerminal.as_view()), name='close'),
    ]