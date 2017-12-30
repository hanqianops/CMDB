# coding: utf-8
__author__ = "HanQian"

from django.db.models import Q
from asset.app_config import site


class FilterSearch(object):
    def __init__(self, request,model_name):
        self.request = request
        self.model_name = model_name

    def _search_field(self):
        search_text = self.request.GET.get("search")
        search_obj = Q()
        if search_text:
            search_obj.connector = "OR"
            for search_field in site.apps['asset'][self.model_name].search_fields:
                search_obj.children.append(("%s__contains" % search_field, search_text))
        return search_obj

    def _status_field(self):
        status_id = self.request.GET.get("status")
        status_obj = Q()
        if status_id:
            status_obj.children.append(('device_status', status_id))
        return status_obj

    def project_module_list(self):
        project_id = self.request.GET.get("project_id")
        module_id = self.request.GET.get("module_id")
        obj = Q()
        if module_id:
            obj.connector = 'OR'
            obj.children.append(('business_unit_id', module_id))
            obj.children.append(('business_unit__parent_unit_id', module_id))
        elif project_id:
            obj.connector = 'OR'
            obj.children.append(('business_unit_id', project_id))  # 一级分组
            obj.children.append(('business_unit__parent_unit_id', project_id))  # 二级分组
            obj.children.append(('business_unit__parent_unit_id__parent_unit_id', project_id))


        obj.add(self._search_field(), "AND")
        obj.add(self._status_field(), "AND")
        return obj