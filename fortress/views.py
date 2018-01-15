import json

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import View

from fortress.interactive import get_redis_instance


def terminal(request):
    return render(request,'fortress/terminal.html',locals())


class CloseTerminal(View):
    def post(self, request):
        if request.is_ajax():
            channel_name = request.POST.get('channel_name', None)
            queue = get_redis_instance()
            redis_channel = queue.pubsub()
            queue.publish(channel_name, json.dumps(['close']))
            return JsonResponse({'status': True, 'message': 'Terminal has been killed !'})
        return JsonResponse({'status': False, 'message': 'Request object does not exist!'})

    def get(self,req):
        return HttpResponse('test')
