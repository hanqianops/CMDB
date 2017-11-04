# coding: utf-8
__author__ = "HanQian"

from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from asset.models import *


def validate_begins(value):
    """自定义验证器"""
    if not value.startswith(u'new'):
        raise ValidationError(u'字符串必须是 `new` 开头')


class ServerForm(ModelForm):
    # 使用自定义的字段
    # name = MyFormField(max_length=200, required=False, validators=[validate_slug]
    # def __init__(self, *args, **kwargs):
    #     print("执行顺序1：init")
    #     # 自定义ModelForm中的field验证规则
    #     super(AuthorForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = True
    #     self.fields['city'].validators.append(validate_begins)
    #
    # def clean_name(self):
    #     """自定义验证方法"""
    #     print("执行顺序2：clean_name")
    #     value = self.cleaned_data['name']
    #     if value == 'root':
    #         return value
    #     else:
    #         raise ValidationError("你不是管理员！")
    #
    # def clean(self):
    #     print("执行顺序3: name")
    #     # 不符合需求的字段不会出现在cleaned_data中
    #     cleaned_data = super(AuthorForm, self).clean()
    #     password = cleaned_data.get('password', '')
    #     password2 = cleaned_data.get('password2', '')
    #     if password != password2:
    #         raise forms.ValidationError("passwords not match")
    #     return cleaned_data

    class Meta:
        print("启动Django时就执行了")
        model = Server

        fields = '__all__'  # 显示全部字段
        # exclude = 'title'   # 排除某个字段
        # fields = ['name', 'title', 'city', ]  # 决定显示哪些字段与显示顺序
        # model中指定editable=False时，任何表单都不会包含该字段。
        # labels = {'name': _('姓名'), }
        # help_texts = {'name': _('Some useful help text.'), }
        # error_messages = {
        #     'name': {'required': _("This writer's name is too long."), },
        #     'birth_date': {'required': _("时间不能为空"), },
        # }


# 与上边具有相同的功能，只是save()方法不同
# from django import forms
#
#
# class AuthorForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     title = forms.CharField(max_length=3,
#                             widget=forms.Select(choices=TITLE_CHOICES))
#     birth_date = forms.DateField(required=False)