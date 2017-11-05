# coding: utf-8
__author__ = "HanQian"

from django import template
from django.utils.safestring import mark_safe
from asset.app_config import site
print(site.apps['asset']['server'].list_display,"====")
register = template.Library()  # register变量名是固定点


@register.filter(is_safe=True)  # 只能接受两个参数
def filter_multi(var, bar):  # var是变量值， bar是选项值
    return var * bar  # {{ value|filter_multi:3 }}


@register.simple_tag
def thead(model_name,row_obj):
    html_str = "<tr>"
    for display_field in site.apps['asset'][model_name].list_display:
        field = display_field.split('.')
        if len(field) == 1:
            field_obj = row_obj._meta.get_field(field[0])
        else:
            field_obj = getattr(row_obj,field[0])
            field_obj = field_obj._meta.get_field(field[1])
        html_str += "<th>{0}</th>".format(field_obj.verbose_name)
    html_str += "</tr>"
    return mark_safe(html_str)

@register.simple_tag
def tbody(model_name,obj_list,page_obj):
    html_str = ""
    for row in obj_list:
        tr_str = "<tr>"
        for display_field in site.apps['asset'][model_name].list_display:
            field = display_field.split('.')
            if len(field) == 1:
                tr_str += "<td>{0}</td>".format(getattr(row,field[0]))
            else:
                try:
                    field_obj = getattr(row, field[0])
                    tr_str += "<td>{0}</td>".format(getattr(field_obj,field[1]))
                except Exception as e:
                    tr_str += "<td></td>"

        tr_str += "</tr>"
        html_str += tr_str
        print(page_obj, "====")
    return mark_safe(html_str)