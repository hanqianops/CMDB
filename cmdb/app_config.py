# coding: utf-8
__author__ = "HanQian"

from cmdb import settings

for app_name  in settings.INSTALLED_APPS:
    try:
        __import__( "%s.%s" %(app_name,"app_config"))
    except ImportError:
        pass