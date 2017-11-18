# coding: utf-8
__author__ = "HanQian"
from cmdb.base import BaseAdmin, site
from asset import models
from django import forms


class ServerAdmin(BaseAdmin):
    list_display = ("name", "inner_ip", "os_type", "os_release", "cabinet.cabinet_num", "device_status")
    # list_display = [("name", "主机名"), ("inner_ip", "内网IP"), ("os_type", "操作系统"),
    #                 ("os_release", "系统版本"), ("asset.cabinet_num", "机柜"), ("device_status", "设备状态"),
    #                 ]
    list_editable = ('name', 'cabinet', 'device_status', 'server_type', 'upper_layer', 'switch')
    readonly_fields = ("name",)
    # widgets = {
    #     "name": forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
    # }
    search_fields = ("name", "inner_ip")


class NetworkAdmin(BaseAdmin):
    list_display = ("name", "cabinet.cabinet_num", "vlan_ip", "intranet_ip", "firmware")
    list_editable = ("name", "asset")
    search_fields = ("name", "asset")

class IDCAdmin(BaseAdmin):
    list_display = ("name", "address", "start_date", "end_date", "memo")
    list_editable = ("name", "address")
    search_fields = ("name", "address")


class CabinetAdmin(BaseAdmin):
    list_display = ("idc", "cabinet_num", "device_type_id", "tag")
    search_fields = ("name", "address")


site.register(models.Server, ServerAdmin)
site.register(models.IDC, IDCAdmin)
site.register(models.Cabinet, CabinetAdmin)
site.register(models.NetworkDevice, NetworkAdmin)
