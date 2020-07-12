import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ZhiFou import settings
from users.models import User
from users.utils.token_op import create_email_token


# 发送邮件，忘记密码
# 无需token认证
@csrf_exempt
def send_email_reset_password(request):
    if request.method == "POST":
        json_req = json.loads (request.body)
        email = json_req['email']
        try:
            user = User.objects.get (email=email)
        except:
            return HttpResponse (json.dumps ({'code': 400, 'info': '找不到邮箱对应用户'}))
        try:
            token = create_email_token (user)
        except:
            return HttpResponse (json.dumps ({'code': 401, 'info': 'token生成失败'}))
        try:
            text = "尊敬的" + user.user_name + \
                   ",你好:\n " \
                   "\t\t\t\t您收到这封电子邮件是因为您 (也可能是某人冒充您的名义) 申请了一个找回密码的请求。\n" \
                   " \t\t\t\t假如这不是您本人所申请, 或者您曾持续收到这类的信件骚扰, 请您尽快联络管理员。\n" \
                   " \t\t\t\t您可以点击如下链接重新设置您的密码,如果点击无效，请把下面的代码拷贝到浏览器的地址栏中：\n" \
                   " \t\t\t\thttp://192.168.8.70:8080/#/sentPassword?token=" + token + "\n" \
                   " \t\t\t\t在访问链接之后, 您可以重新设置新的密码。"
            send_mail (subject='知否密码找回',
                       from_email=settings.EMAIL_HOST_USER,
                       recipient_list=[email],
                       fail_silently=False, message=text)
        except:
            return HttpResponse (json.dumps ({'code': 402, 'info': '邮件发送失败'}))  # 发送失败
        return HttpResponse (json.dumps ({
            'code': 200,
            'user_id': user.user_id,
            'user_account': user.user_account,
            'email': user.email
        }))  # 用户信息
    else:
        return HttpResponse (json.dumps ({'code': 404, 'info': '请求非post'}))  # 请求非post
