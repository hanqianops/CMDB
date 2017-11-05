from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "asset/base.html")

from asset.forms import ServerForm
from asset import models
from django.views.generic.edit import FormView
from django.views.generic import View
from django.views.generic import ListView

class Before(object):
    def dispatch(self, request, *args, **kwargs):
        print("请求之前执行")
        if request.GET.get("page_num"):
            request.session['page_num'] = request.GET.get("page_num")
        elif not request.session.get("page_num"):
            request.session['page_num'] = 3
        self.paginate_by = int(request.session['page_num'])

        print(request.session.__dict__, "ssssssssssssss")
        obj = super(Before, self).dispatch(request, *args, **kwargs)
        print(request.GET)

        return obj


class AssetList(Before,ListView):
    template_name = "asset/asset_list.html"
    model = models.Server


    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        print(self.paginate_by,"=====----")
        return context


