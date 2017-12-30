# coding: utf-8
__author__ = "HanQian"

from asset import models
import json

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

    def session(self):
        self.request.session['url_list'] = self.get_privileged_url()
        self.request.session['role_list'] = self.get_role()

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
print(json.dumps(d,indent=4,ensure_ascii=False))