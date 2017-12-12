from cmdb import settings
from django.core.signals import request_finished
from django.core.signals import request_started
from django.core.signals import got_request_exception

from django.db.models.signals import class_prepared
from django.db.models.signals import pre_init, post_init
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_delete, post_delete
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_migrate, post_migrate

from django.test.signals import setting_changed
from django.test.signals import template_rendered

from django.db.backends.signals import connection_created


def callback(sender, **kwargs):
    print("xxoo_callback=========================")
    # print(dir(sender), dir(kwargs))
    # print(sender.__dict__, kwargs)
    # print('Saved: {}'.format(kwargs.__dict__))


request_finished.connect(callback)
for app_name  in settings.INSTALLED_APPS:
    try:
        __import__( "%s.%s" %(app_name,"config"))
    except ImportError:
        pass