from django.shortcuts import render,HttpResponse
from asset import models
from asset import serializers


def login_host(request):
    obj = models.Server.objects.all()
    print(request.session.__dict__,'==========================')
    return render(request,'fortress/loginhost.html',locals())

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.utils.six import BytesIO
def menu(request,user):
    user_obj = models.User.objects.filter(username=user)
    serializer = serializers.UserSerializer(user_obj,many=True)
    content = JSONRenderer().render(serializer.data)
    stream = BytesIO(content)
    data = JSONParser().parse(stream)
    a = json.dumps(data,ensure_ascii=False)
    data = a.replace('parent_unit','pId')
    data = json.loads(data)[0]
    r=[]
    for node in data['businessunit']:
        # print(node)
        for se in node['server_set']:
            se["pId"] = node['id']
            r.append(se)
            print("se===",se)
        if node['server_set'] != None:
            node.pop("server_set")
            if node['pId'] is None:
                node['pId'] = 0
            r.append(node)
            print("node===",node)

    print(r)
    return HttpResponse(data)