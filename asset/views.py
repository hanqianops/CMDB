from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "asset/base.html")

from asset.forms import ServerForm
from asset import models
from django.views.generic.edit import FormView
from django.views.generic import ListView
class AssetList(ListView):
    template_name = "asset/base.html"
    model = models.Server


