from cmdb import settings

for app_name  in settings.INSTALLED_APPS:
    try:
        __import__( "%s.%s" %(app_name,"config"))
    except ImportError:
        pass