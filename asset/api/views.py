# coding: utf-8
__author__ = "HanQian"

from rest_framework.decorators import api_view
from  rest_framework import generics
from ..models import Server,BusinessUnit,User
from asset.serializers import ServerSerializer,UserSerializer
from rest_framework.response import Response
from django.http import HttpResponse


class ServerListView(generics.ListAPIView):
    queryset = Server.objects.all()   # 基础查询集,用来取对象
    serializer_class = ServerSerializer  # 用来序列化对象

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer