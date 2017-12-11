# coding: utf-8
__author__ = "HanQian"


def gg(request,):
    context = {
        "last_url":  request.META.get('HTTP_REFERER'),
        "title": 'sss',
    }
    return context