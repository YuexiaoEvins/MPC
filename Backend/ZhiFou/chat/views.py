# chat/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect, request, HttpResponse
from django.utils.safestring import mark_safe
from users.utils.token_op import checkToken
from django.views.decorators.csrf import csrf_exempt
import json

# def index(request):
#     return render(request, 'chat/index.html', {})

def room(request,from_id,to_id):
    return render(request, 'chat/room.html', {
        'from_id': from_id,
        'to_id':to_id,
    })

@csrf_exempt
@checkToken("")
def checkChatToken(request):
    return HttpResponse(json.dumps({
        'code':200,
    }))

#获得聊天记录接口