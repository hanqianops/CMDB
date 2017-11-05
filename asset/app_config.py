# coding: utf-8
__author__ = "HanQian"
from cmdb.base import BaseConfig, site
from asset import models
class Server(BaseConfig):
    list_display = ("name","inner_ip", "asset.cabinet_num")


site.register(models.Server,Server)
