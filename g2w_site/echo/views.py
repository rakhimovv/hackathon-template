import sys

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

sys.path.append('..')

from g2w_rabbitmq.rpc_client import RpcClient

rpc = None


def index(request):
    global rpc
    rpc = RpcClient()
    return render(request, 'index.html')


@csrf_exempt
def handle(request):
    if request.method == "POST":
        text = request.POST['text']
        data = {
            'status': 'ok',
            'result': str(rpc.call(text), "utf-8"),
        }
        return JsonResponse(data)
