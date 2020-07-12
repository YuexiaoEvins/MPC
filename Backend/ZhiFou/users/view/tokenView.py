import json

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users.utils.token_op import check_token, get_userid

TIME_OUT = 60 * 60 * 24 * 7  # 过期时间 7天


# 验证token，通过用户id
# 获取当前cache中userid对应的token
# 比较两个token是否相同
@csrf_exempt
def check_token_validity(request):
    if request.method == 'POST':
        # 解token 查找用户
        json_req = json.loads (request.body)
        token = json_req['token']
        if check_token (token):
            user_id = get_userid (token)
            cache.set (user_id, token, TIME_OUT)
            return HttpResponse (json.dumps ({'code': 200, 'info': 'token有效'}))
        else:
            return HttpResponse (json.dumps ({'code': 401, 'info': 'token失效'}))
    else:
        return HttpResponse (json.dumps ({'code': 404, 'info': '请求非post'}))
