# coding: utf-8
__author__ = "HanQian"


def get_parameter(request, current_param):
    """处理url请求的参数"""
    temp = []
    parameter = ["page", "page_num", "project_id", "module_id"]
    for key in parameter:
        value = request.GET.get(key)
        if value and key not in current_param:
            temp.append("=".join([key, str(value)]))
    print("sss", "&".join(temp))
    return "&".join(temp)  # page=2&page_num=3&project=1&module=3