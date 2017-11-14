# coding: utf-8
__author__ = "HanQian"
from cmdb.base import BaseConfig, site
from asset import models
class ServerAdmin(BaseConfig):
    list_display = ("name","inner_ip", "os_type","os_release","asset.cabinet_num","device_status")
    search_fields = ("name","inner_ip")

class IDCAdmin(BaseConfig):
    list_display = ("name","address", "start_date","end_date","memo")
    search_fields = ("name","address")

site.register(models.Server,ServerAdmin)
site.register(models.IDC,IDCAdmin)
