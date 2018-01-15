# coding: utf-8
__author__ = "HanQian"

def get_redis_instance():
    from fortress.asgi import channel_layer
    return channel_layer._connection_list[0]


if __name__ == '__main__':
    import os, sys
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')
    get_redis_instance()