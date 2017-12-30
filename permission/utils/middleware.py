# coding: utf-8
__author__ = "HanQian"

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect
from permission import views
class PermissionAuth(MiddlewareMixin):
    def process_request(self, request):
        print('process_request=====',request.path)
        if request.path in ('/login/', '/logout/'):
            return None
        if request.session.get('user'):
            if '超级管理员' in request.session.get('role_list'):
                return None
            if request.path in request.session.get('url_list'):
                return None
            else:
                return HttpResponse('<h3>无权限访问</h3>')
        else:
            return redirect('/login/')

    def process_response(self, request, response):
        print('process_response=====',request.path)
        return response