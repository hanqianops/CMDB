# coding: utf-8
__author__ = "HanQian"

from rest_framework import serializers
from asset.models import *
from django.contrib.auth.models import User


class MemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mem
        fields = '__all__'

class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = '__all__'

class ServerSerializer(serializers.ModelSerializer):
    mem = MemSerializer(many=True,)
    class Meta:
        model = Server
        fields = '__all__'

class UserServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id','name','inner_ip')

class UserBusinessUnitSerializer(serializers.ModelSerializer):
    server_set = UserServerSerializer(many=True)
    class Meta:
        model = BusinessUnit
        fields = ('id','name','parent_unit','server_set')

class UserSerializer(serializers.ModelSerializer):
    businessunit = UserBusinessUnitSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username','businessunit')
        # class SnippetSerializer2(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance