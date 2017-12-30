# coding: utf-8
__author__ = "HanQian"
#  responsefrom django.utils.deprecation import MiddlewareMixin
# from django.http import HttpResponse
# class ddd(MiddlewareMixin):
#     def process_request(self, request):
#         print('process_request=====',request.path)
#         return None
#
#     def process_view(self,request,index,callback_args,callback_kwargs):
#         print('.............')
#
#     def process_response(self, request, response):
#         print('process_response=====',request.path)
#
#         return

class D(object):
    def g(self):
        return 111
    def h(self):
        f = self.g()
        print(f)

d = D()
d.h()