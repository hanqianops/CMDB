from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from asset.models import User
from cmdb import settings
from permission.utils.permission import PermissionInit
from django.conf import settings
import hashlib


class LoginView(View):
    def get(self,request):
        next_url = request.META.get('HTTP_REFERER','/')
        return render(request,'registration/login.html',locals())

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        print("password:", password)
        print("password:", username)
        hash = hashlib.md5(bytes(request.POST['password'], encoding='utf-8'))
        hash.update(bytes(settings.USER_PASSWORD_SALT, encoding='utf-8'))
        password = hash.hexdigest()
        user = User.objects.get(username=username,password=password)
        if user:
            request.session['user'] = username
            request.session['full_name'] = user.full_name or user.username
            p = PermissionInit(request)
            p.session()
            return redirect(settings.LOGIN_URL)
        else:
            login_validate = "用户名密码错误"
            return render(request,'registration/login.html',locals())


