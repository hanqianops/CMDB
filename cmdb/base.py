# coding: utf-8
__author__ = "HanQian"

class BaseConfig(object):

    list_display = ()
    list_filter = ()
    search_fields = ()
    list_per_page = 5
    actions = ()
    readonly_fields = ()

class AppSite(object):
    def __init__(self):
        self.apps = {}

    def register(self, model_obj,config=BaseConfig, **options):
        """
        负责把每个App下的表加载到self.apps里
        """
        config = config()
        # admin_class.model.objects.filter() == models.xxx.objects.filter()
        config.obj = model_obj

        app_label = model_obj._meta.app_label
        if app_label not in self.apps:
            self.apps[app_label] =  {}
        self.apps[app_label][model_obj._meta.model_name] = config

site = AppSite()