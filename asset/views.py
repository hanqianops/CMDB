import json

from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from asset.app_config import site
from asset.forms import create_modelform, create_modelformset
from asset.plugins.page import PageInfo
from asset.plugins.filter import FilterSearch


def index(request):
    return render(request,'asset/eee.html',locals())

class Before(object):
    def dispatch(self, request, *args, **kwargs):
        self.model_name = self.kwargs['model_name']
        self.admin_class = site.apps['asset'][self.model_name]
        self.model = site.apps['asset'][self.model_name].model
        self.title = self.model._meta.verbose_name
        request.session['display_field'] = request.GET.get('display_field')
        # print("session对象", request.session.__dict__, )
        # print("COOKIES对象", request.COOKIES)
        # print("请求的路径", request.path_info)
        obj = super(Before, self).dispatch(request, *args, **kwargs)
        return obj

class AssetList(Before, ListView):
    template_name = "list.html"

    def get_queryset(self):
        obj = FilterSearch(self.request,self.model_name)
        obj_list = self.model.objects.filter(obj.project_module_list())
        current_page = self.request.GET.get("page")

        self.page_info = PageInfo(
            self.request, obj_list,
            current_page,
            per_page_num=self.request.GET.get("page_num") or 10
        )
        obj_list = obj_list[self.page_info.start:self.page_info.end]
        return obj_list

    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        # context.update(gg(self.request,Before()))
        context['model_name'] = self.kwargs['model_name']
        context['page_info'] = self.page_info
        context['title'] = self.model._meta.verbose_name
        context['admin_class'] = self.admin_class
        return context


class AssetDetail(Before,DetailView):

    def get(self, request, *args, **kwargs):
        object = self.model.objects.get(id=kwargs['id'])
        model_name=self.model_name
        title = self.model._meta.verbose_name
        return render(request,'detail.html',locals())



class AssetDelete(Before,View):
    def post(self, request, *args, **kwargs):
        # return HttpResponseRedirect('/asset/server')
        dic = {"status": False}
        return HttpResponse(json.dumps(dic))

    def get(self, request, *args, **kwargs):
        dic = {"status": True}
        object = self.model.objects.filter(id=kwargs['pk']).values('name', 'id')
        if object:
            dic.update(object[0])
        else:
            dic['status'] = False
        print(json.dumps(dic))
        return HttpResponse(json.dumps(dic))


class AssetCreate(Before, View):

    def get(self, request, model_name):
        form = create_modelform(self.model)
        last_url = request.META.get('HTTP_REFERER')
        title = self.model._meta.verbose_name
        return render(request, "create.html", locals())

    def post(self, request, model_name):
        dict = {"status": True, "error": None}
        modelform = create_modelform(self.model)
        form = modelform(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "create.html", locals())
        skip = reverse('asset:list', kwargs={"model_name": self.model_name})
        return HttpResponseRedirect(skip)



class AssetUpdate(Before, View):
    permission_required = 'businessunit.change_businessunit'
    def get(self, request, model_name):
        title = self.model._meta.verbose_name
        obj_id_list = request.GET.get("id").split(',')
        obj_list = self.model.objects.filter(id__in=obj_id_list)
        modelformset = create_modelformset(self.model, self.admin_class.list_editable)
        formset = modelformset(queryset=obj_list)
        return render(request, "edit.html", locals())

    def post(self, request, model_name):
        modelformset = create_modelformset(self.model, self.admin_class.list_editable)
        formset = modelformset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            return render(request, "edit.html", locals())
        skip = reverse('asset:list', kwargs={"model_name": self.model_name})
        return HttpResponseRedirect(skip)



"""
In [36]: project_list=Q()

In [37]: project_list.children.append(('business_unit__parent_unit_id',1))

In [38]: models.Server.objects.filter(project_list)
Out[38]: <QuerySet [<Server: retail-gms-001>, <Server: retail-pos-001>, <Server: retail-pos-002>]>




module_list = Q()
module_list.children.append(('business_unit_id',1))
models.Server.objects.filter(module_list)
"""
