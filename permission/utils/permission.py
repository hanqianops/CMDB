# coding: utf-8
__author__ = "HanQian"

from asset import models
import json
from django.shortcuts import HttpResponse,redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from asset import models
from asset import serializers

class PermissionInit(object):
    def __init__(self,request):
        self.request = request
        self.user = self.request.session.get('user')
        self.per_list =list(models.User.objects.filter(username=self.user,).values('roles__name','roles__permissions__url','roles__permissions__menu__name','roles__permissions__menu__order'))
    def get_role(self):
        """获取用户角色"""
        role_list = set()
        for item in self.per_list:
            role_list.add(item['roles__name'])
        self.request.session['role_list'] = list(role_list)
        return list(role_list)

    def get_privileged_url(self):
        """获取有权限的URL"""
        url_list = []
        for item in self.per_list:
            url = item['roles__permissions__url']
            url_list.append(url)
        print("可访问的URL:",url_list)
        self.request.session['url_list'] = url_list
        return url_list

    def host_menu(self):
        user_obj = models.User.objects.filter(username=self.user)
        serializer = serializers.UserSerializer(user_obj, many=True)
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        a = json.dumps(data, ensure_ascii=False)
        data = a.replace('parent_unit', 'pId')
        data = json.loads(data)[0]
        r = []
        for node in data['businessunit']:
            for se in node['server_set']:
                se["pId"] = node["id"]
                r.append(se)
            if node['server_set'] != None:
                node.pop("server_set")
                if node['pId'] is None:
                    node['pId'] = 0
                r.append(node)
        self.request.session["host_menu"] = r
    def session(self):
        self.get_privileged_url()
        self.get_role()
        self.host_menu()
        # self.request.session['url_list'] =
        # self.request.session['role_list'] =

    def get_menu(self):
        """获取有访问权限的菜单"""
        menu_list = []
        for item in self.per_list:
            url = item['roles__permissions__url']
            name = item['roles__permissions__menu__name']
            order = item['roles__permissions__menu__order']
            if name:
                if url.endswith('/'):
                    menu_item = {
                        "name": name,
                        "url": url,
                        "order": order
                    }
                    menu_list.append(menu_item)
            return menu_list


q =list(models.User.objects.filter(username='han',).values('roles__name','roles__permissions__url','roles__permissions__menu__name','roles__permissions__menu__order'))
d = {}

for i in q:
    url = i['roles__permissions__url']
    roles = i['roles__name']
    menu_name = i['roles__permissions__menu__name']
    menu_order = i['roles__permissions__menu__order']

    d.setdefault('roles',[]).append(i['roles__name'])
    if url:
        d.setdefault('url', []).append(url)
    if menu_name:
        if url.endswith('/'):
            d.setdefault('menu',[]).append({'name':menu_name.split('-')[-1],
                                            'url':url,
                                            'order':menu_order
                                            })
d['roles'] = list(set(d['roles']))
# print(json.dumps(d,indent=4,ensure_ascii=False))