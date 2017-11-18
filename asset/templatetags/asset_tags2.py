# coding: utf-8
__author__ = "HanQian"

from django import template
from django.utils.safestring import mark_safe
from asset.app_config import site
from asset.models import BusinessUnit
from asset.plugins.get_url import get_parameter

print(site.apps['asset']['server'].model.device_status_choices, "==00000==")
register = template.Library()  # register变量名是固定点


@register.filter(is_safe=True)  # 只能接受两个参数
def filter_multi(var, bar):  # var是变量值， bar是选项值
    return var * bar  # {{ value|filter_multi:3 }}




@register.simple_tag
def thead(model_name,):
    list_display = site.apps['asset'][model_name].list_display
    html_str = ""
    for _,display_name in list_display:
        html_str += "<th>{0}</th>".format(display_name)
    return mark_safe(html_str)


@register.simple_tag
def tbody(model_name, obj_list, page_obj):
    list_display = site.apps['asset'][model_name].list_display
    html_str = ""
    for row in obj_list:
        tr_str = """<tr>
                        <td><label><input type="checkbox" ><span class="text"></span></label></td>
                        <td>{0}</td>
                        """.format(row.id)
        for display_field,_ in list_display:
            field = display_field.split('.')
            try:
                field_obj = getattr(row, field[0])
                if len(field) == 1:
                    if row._meta.get_field(field[0]).choices:
                        f = 'get_{0}_display'.format(field[0])
                        tr_str += "<td>{0}</td>".format(getattr(row, f)())
                    else:
                        tr_str += "<td>{0}</td>".format(getattr(row, field[0]))
                else:

                    if field_obj._meta.get_field(field[1]).choices:
                        f = 'get_{0}_display'.format(field[1])
                        tr_str += "<td>{0}</td>".format(getattr(field_obj,f)())
                    else:
                        tr_str += "<td>{0}</td>".format(getattr(field_obj, field[1]))
            except Exception as e:
                tr_str += "<td></td>"

        tr_str += """<td>
                    <a href="{id}/" > 详细信息 |</a>
                    <a href='javascript:void(0)' onclick='modalObj({id});'> 删除</button>
                    </td></tr>""".format(**{"id":row.id,"row":row})
        html_str += tr_str
    return mark_safe(html_str)

@register.assignment_tag
def ff():
    value3 = [
        {"title": "aaa"},
        {"title": "bbb"},
        {"title": "ccc"}
    ]
    return {"value": value3}



@register.simple_tag
def project(request):
    """
     <div class="DTTT btn-group">
        <a id="projectButton" class="btn btn-default " href="javascript:void(0);">全部项目</a>
        <a class="btn btn-default  dropdown-toggle" data-toggle="dropdown"
           href="javascript:void(0);"><i class="fa fa-angle-down"></i></a>
        <ul class="dropdown-menu dropdown-inverse">
            <li><a href="/asset/server/?project_id=0">全部项目</a></li>
            <li><a href="/asset/server/?project_id=1">零售项目</a></li>
            <li><a href="/asset/server/?project_id=4">会员项目</a></li>
            <li><a href="/asset/server/?project_id=5">物流项目</a></li>
            <li class="divider"></li>
        </ul>
     </div>
    :return:
    """
    parameter = get_parameter(request, ("project_id","module_id"))
    business_obj = BusinessUnit.objects.filter(parent_unit_id__isnull=True).values('id', 'name')
    html_business = "<li><a href='?'>全部项目</a></li>"
    for b_obj in business_obj:
        html_business += '<li><a href="?project_id={id}&{0}">{name}</a></li>'.format(parameter,**b_obj)
    return mark_safe(html_business)


@register.simple_tag
def module(request):
    module_id = get_parameter(request,("module_id",))
    project_id = request.GET.get("project_id")
    if project_id:
        module_obj_list = BusinessUnit.objects.filter(parent_unit_id=project_id).values('id', 'name')
        html_module = "<li><a href='?project_id={0}'>全部模块</a></li>".format(project_id)

    else:
        module_obj_list = BusinessUnit.objects.filter(parent_unit_id__isnull=False).values('id', 'name')
        html_module = "<li><a href='?'>全部模块</a></li>"

    for m_obj in module_obj_list:
        html_module += '<li><a href="?module_id={id}&{0}">{name}</a></li>'.format(module_id,**m_obj,)
    return mark_safe(html_module)

@register.simple_tag
def status(model_name,request):
    module_id = get_parameter(request, ("module_id",))
    project_id = request.GET.get("project_id")
    # models.Server.device_status_choices
    L = site.apps['asset'][model_name].model.device_status_choices
    html_status = "<li><a href='?'>全部状态</a></li>"
    for id,name in L:
        html_status += "<li><a onclick='FilterStatus({0})'>{1}</a></li>".format(id,name)
        print(id,name)
    return mark_safe(html_status)