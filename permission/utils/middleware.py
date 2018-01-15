# coding: utf-8
__author__ = "HanQian"

import json

from django.shortcuts import HttpResponse,redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from asset import models
from asset import serializers


class PermissionAuth(MiddlewareMixin):
    def process_request(self, request):
        print('process_request=====',request.path)
        if request.path in ('/login/', '/logout/'):
            return None
        if request.session.get('user'):
            if '超级管理员' in request.session.get('role_list'):
                return None
            print( request.path.split("?")[0],request.session.get('url_list'))
            if request.path.split("?")[0] in request.session.get('url_list'):
                return None
            else:
                return HttpResponse('<h3>无权限访问</h3>')
        else:
            return redirect('/login/')

    def process_response(self, request, response):
        print('process_response=====',request.path)
        return response