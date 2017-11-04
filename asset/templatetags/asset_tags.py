# coding: utf-8
__author__ = "HanQian"

from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register变量名是固定点


@register.filter(is_safe=True)  # 只能接受两个参数
def filter_multi(var, bar):  # var是变量值， bar是选项值
    return var * bar  # {{ value|filter_multi:3 }}


@register.simple_tag
def asset_list(obj_list):
    for obj in obj_list:
        print(obj.inner_ip)
    temp='sad'
    return mark_safe(temp)