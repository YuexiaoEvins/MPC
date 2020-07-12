# login用户登录，生成token
# 接收JSON数据
# user_account 用户输入用户名
# password 用户输入的密码
import json

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserForm
from users.models import User

from users.utils import token_op
from users.view.captchaView import judge_captcha
from users.views import add_address_profile_url


@csrf_exempt
def login(request):
    if request.method == "POST":
        login_req = json.loads (request.body)
        user_account = login_req['user_account']
        password = login_req['password']
        try:
            user = User.objects.get (user_account=user_account)
        except:
            return HttpResponse (json.dumps ({'code': '401', 'info': '用户不存在'}))  # 用户不存在
        if check_password (password, user.password):
            temp = user
            token = token_op.create_token (temp)
            return HttpResponse (
                json.dumps (
                    {
                        'code': '200',  # 成功状态码
                        'token': token,
                        'user_id': user.user_id,
                        'user_account': user.user_account,
                        'user_url': add_address_profile_url(user.user_url),
                        'user_name': user.user_name,
                        'user_gender': user.user_gender,
                        'email': user.email,
                        'user_phone': user.user_phone,
                        'user_credit': user.user_credit,
                        'status': user.status,
                    }
                )
            )
        else:
            return HttpResponse (json.dumps ({'code': '402', 'info': '密码不正确'}))  # 密码不正确
    else:
        return HttpResponse (json.dumps ({'code': '404', 'info': '请求非post'}))  # 请求非POST类型


# 用户登录接口
# 在前端请求验证码生成之后调用
@csrf_exempt
def login_demo(request):
    if request.method == "POST":
        login_req = json.loads (request.body)
        user_account = login_req['user_account']
        password = login_req['password']
        captcha_0 = login_req['hashkey']
        captcha_1 = login_req['captcha_1']
        print(len(captcha_1))
        # if len(captcha_1) == 0:
        #     return HttpResponse (json.dumps ({'code': '405', 'info': '验证码输入为空'}))  # 用户不存在
        # if judge_captcha(captcha_1, captcha_0):
        try:
            user = User.objects.get (user_account=user_account)
        except:
            return HttpResponse (json.dumps ({'code': '401', 'info': '用户不存在'}))  # 用户不存在
        if check_password (password, user.password):
            temp = user
            token = token_op.create_token (temp)
            return HttpResponse (
                json.dumps (
                    {
                        'code': '200',  # 成功状态码
                        'token': token,
                        'user_id': user.user_id,
                        'user_account': user.user_account,
                        'user_url': add_address_profile_url(user.user_url),
                        'user_name': user.user_name,
                        'user_gender': user.user_gender,
                        'email': user.email,
                        'user_phone': user.user_phone,
                        'user_credit': user.user_credit,
                        'status': user.status,
                    }
                )
            )
        else:
            return HttpResponse (json.dumps ({'code': '402', 'info': '密码不正确'}))  # 密码不正确
        # else:
        #     return HttpResponse (json.dumps ({'code': '403', 'info': '验证码/hashkey有误'}))  # 验证码错误
    else:
        return HttpResponse (json.dumps ({'code': '404', 'info': '请求非post'}))  # 请求非POST类型


