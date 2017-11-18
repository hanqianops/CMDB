# # coding: utf-8
# __author__ = "HanQian"
#

from django.utils.translation import ugettext_lazy as _
from asset.models import *

from django.utils.html import escape,format_html
from django.utils.html import escape,format_html
from django.utils.encoding import force_text
from django.forms.utils import flatatt
from asset.app_config import site
from asset import models
from django.forms import ModelForm, TextInput
from django import forms
from django.forms.models import modelformset_factory
print(site.apps['asset']['server'].model.device_status_choices, "ModelForm")




def __new__(cls,*args,**kwargs):
    for field_name in cls.base_fields:
        if field_name.endswith("date"):
            cls.base_fields[field_name].widget = forms.DateTimeInput(attrs={'type': 'date'})
        elif field_name == 'memo':
            cls.base_fields[field_name].widget = forms.Textarea(attrs={'class':'form-control'})
        cls.base_fields[field_name].widget.attrs.update({'class':'form-control'})
    return ModelForm.__new__(cls)


def create_modelform(model_obj,fields=None,labels=None):
    """
    动态创建ModelForm，提供一个用于创建新数据的表单
    :param model_obj:  model对象
    :param fields: 创建新数据时可以创建的字段
    :param labels: 字段显示名
    :return:  返回一个ModelForm对象
    """
    class Meta: pass
    Meta.model = model_obj
    Meta.fields = fields or ('__all__')
    Meta.labels = labels

    modelform = type("modelform",(ModelForm,),{'__new__':__new__,'Meta':Meta})
    return modelform


def create_modelformset(model_obj,list_editable=None,labels=None):
    """
    根据请求的model对象动态创建表单集，实现批量编辑功能
    :param model_obj:
    :param list_editable:  可以编辑的字段
    :param labels:
    :return:
    """
    modelform = create_modelform(model_obj,fields=list_editable,labels=labels)
    modelformset = modelformset_factory(model_obj, form=modelform,max_num=1)
    return modelformset

#
# def edit_form(admin_class):
#     """生成编辑表单"""
#     dic = {
#         "form": ServerForm,
#         #"fields": admin_class.list_editable,
#         "max_num" : 1,
#     }
#     return modelformset_factory(admin_class.model, **dic)





#
# d = {
#     "fields": ('id','name', 'asset', 'device_status', 'server_type', 'upper_layer', 'switch'),
#             "max_num": 1,
#             "widgets":{
#                 "name": forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
#             }
# }
# EditSeverFormSet = modelformset_factory(
#             Server,
#           **d
#         )
#
# class ServerForm(ModelForm):
#
#     def __init__(self,*args,**kwargs):
#         super(ServerForm, self).__init__(*args, **kwargs)
#         for field_name in self.base_fields:
#
#             if field_name.endswith("date"):
#                 self.base_fields[field_name].widget = forms.DateTimeInput(attrs={'type':'date'})
#             else:
#                 self.base_fields[field_name].widget.attrs['class'] = 'form-control'
#
#         # print(self.base_fields['expire_date'].widget)
#         # print(dir(self.base_fields['name']))
#         # print(self.base_fields['name'])
#         # print(self.base_fields['expire_date'].widget.attrs)
#
#     class Meta:
#         model = models.Server
#         fields = ('__all__')
#         labels = {'asset': _('机柜'), }
#         widgets = {
#         #     "asset": Select(attrs={'class': 'form-control'}),
#             #"name":TextInput(attrs={'class': 'form-control', "readonly":''}),
#         #     "inner_ip":TextInput(attrs={'class': 'form-control',}),
#         #     "management_ip":TextInput(attrs={'class': 'form-control',}),
#         #     "device_status":Select(attrs={'class': 'form-control'}),
#         #     "business_unit":Select(attrs={'class': 'form-control'}),
#         #     "server_type":Select(attrs={'class': 'form-control'}),
#         #     "upper_layer":Select(attrs={'class': 'form-control'}),
#         #     "switch":Select(attrs={'class': 'form-control'}),
#         #     "os_release": TextInput(attrs={'class': 'form-control', }),
#         #     "os_type": TextInput(attrs={'class': 'form-control', }),
#         #     "sn": TextInput(attrs={'class': 'form-control', }),
#         #     "os_type": TextInput(attrs={'class': 'form-control', }),
#         #     "device_type": Select(attrs={'class': 'form-control', }),
#         #     "server_attr": TextInput(attrs={'class': 'form-control', }),
#         #     "trade_date": DateTimeInput(attrs={'type':'date'}),
#         #     "expire_date": DateTimeInput(attrs={'type':'date'}),
#         #     "tags":SelectMultiple(attrs={'class': 'form-control'})
#         }
#         help_texts = {'name': _('Some useful help text.'), }
#         error_messages = {
#             'name': {'required': _("请填写主机名"),'unique':'主机名必须唯一' },
#             'sn': {'required': _("请填写SN"),'unique':'SN必须唯一' },
#             # 'birth_date': {'required': _("时间不能为空"), },
#         }