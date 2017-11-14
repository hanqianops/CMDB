from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "asset/aaa.html")


import json
from asset import models
from django.views.generic.edit import FormView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import FormView
from django.db.models import Q
from asset.app_config import site
from asset.plugins.page import PageInfo
from django.http import HttpResponse, HttpResponseRedirect
from asset import forms
from django.forms.models import modelformset_factory
from asset.forms import EditSeverFormSet,ServerForm

print(site.apps['asset']['server'].list_display)

class Before(object):
    def dispatch(self, request, *args, **kwargs):
        self.model = site.apps['asset'][self.kwargs['model_name']].model
        # print(self.model.model)
        print(self.kwargs['model_name'])
        print("session对象",request.session.__dict__,)
        print("COOKIES对象",request.COOKIES)
        print("请求的路径",request.path_info)
        obj = super(Before, self).dispatch(request, *args, **kwargs)
        return obj

class FilterSearch(object):
    def __init__(self,request):
        self.request = request

    def _search_field(self):
        search_text = self.request.GET.get("search")
        search_obj = Q()
        if search_text:
            search_obj.connector = "OR"
            for search_field in site.apps['asset']['server'].search_fields:
                search_obj.children.append(("%s__contains" % search_field, search_text))
        return search_obj

    def _status_field(self):
        status_id = self.request.GET.get("status")
        status_obj = Q()
        if status_id:
            status_obj.children.append(('device_status',status_id))
        return status_obj



    def project_module_list(self):
        project_id = self.request.GET.get("project_id")
        module_id = self.request.GET.get("module_id")
        obj = Q()
        if module_id:
            obj.children.append(('business_unit_id', module_id))
        elif project_id:
            obj.connector = 'OR'
            obj.children.append(('business_unit__parent_unit_id', project_id))
            obj.children.append(('business_unit_id', project_id)) # 还没二级分组的情况

        obj.add(self._search_field(),"AND")
        obj.add(self._status_field(),"AND")
        return obj


class AssetList(Before,ListView):
    template_name = "asset/asset_list.html"

    def get_queryset(self):
        obj = FilterSearch(self.request)
        print("===",obj.project_module_list())
        obj_list = self.model.objects.filter(obj.project_module_list())
        current_page = self.request.GET.get("page")
        self.page_info = PageInfo(
            self.request,obj_list,
            current_page,
            per_page_num= self.request.GET.get("page_num") or 10
        )
        obj_list = obj_list[self.page_info.start:self.page_info.end]
        return obj_list

    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        context['page_info'] = self.page_info
        return context


class AssetDetail(DetailView):
    model = models.Server
    template_name = 'asset/asset_detail.html'  # 模板
    pk_url_kwarg = 'id'  # PublisherDetail.objects.filter(pk=user_id)

class AssetDelete(View):
    def post(self, request, *args, **kwargs):
        # return HttpResponseRedirect('/asset/server')
        dic = {"status": False}
        return HttpResponse(json.dumps(dic))
    def get(self,request,model_name,pk):
        dic = {"status": True}
        object = models.Server.objects.filter(id=pk).values('name','id')
        if object:
            dic.update(object[0])
        else:
            dic['status'] = False
        print(json.dumps(dic))
        return HttpResponse(json.dumps(dic))

class AssetCreate(View):
    def get(self,request,model_name):
        q = models.Server.objects.filter(id__gt=8)
        form = ServerForm()
        return render(request, "asset/create.html", locals())
    def post(self,request,model_name):
        dict = {"status":True,"error":None}
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "asset/create.html", locals())
        return HttpResponseRedirect('/asset/server/')

class AssetUpdate(View):

    def dispatch(self, request, *args, **kwargs):
        self.url = request.META.get('HTTP_REFERER')
        obj = super(AssetUpdate, self).dispatch(request, *args, **kwargs)
        return obj

    def get(self,request,model_name):
        url = self.url
        edit_obj_list = request.GET.get("id").split(',')
        q = models.Server.objects.filter(id__in=edit_obj_list)
        formset = EditSeverFormSet(queryset=q)
        return render(request, "asset/edit.html", locals())

    def post(self,request,model_name):
        formset = EditSeverFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors,'===============')
            return render(request, "asset/edit.html", locals())
        return HttpResponseRedirect('/asset/server/')

# class AssetUpdate(UpdateView):
#     model = models.Server
#     form_class = forms.ServerForm
#     template_name = 'asset/edit.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(AssetUpdate, self).get_context_data(**kwargs)
#         if '__next__' in self.request.POST:
#             context['i__next__'] = self.request.POST['__next__']
#         else:
#             context['i__next__'] = self.request.META['HTTP_REFERER']
#         return context
#     def get_success_url(self):
#         self.url = self.request.POST['__next__']
#         return self.url


"""
In [36]: project_list=Q()

In [37]: project_list.children.append(('business_unit__parent_unit_id',1))

In [38]: models.Server.objects.filter(project_list)
Out[38]: <QuerySet [<Server: retail-gms-001>, <Server: retail-pos-001>, <Server: retail-pos-002>]>




module_list = Q()
module_list.children.append(('business_unit_id',1))
models.Server.objects.filter(module_list)
"""