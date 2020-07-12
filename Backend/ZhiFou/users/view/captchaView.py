import json

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse

from users.views import add_address_profile_url


# 生成验证码
# 返回hashkey和服务器验证码图片绝对地址
def get_captcha(request):
    # 验证码，第一次请求
    hashkey = CaptchaStore.generate_key ()
    image_url = captcha_image_url (hashkey)
    return HttpResponse (
        json.dumps (
            {
                'hashkey': hashkey,
                'image_url': add_address_profile_url(image_url)
            }
        )
    )


# 验证验证码
def judge_captcha(captchaStr, captchaHashkey):
    if (len(captchaStr) and len(captchaHashkey)) != 0:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get (hashkey=captchaHashkey)
        except:
            # return HttpResponse (json.dumps ({'code': 4401, "info": "hashkey不存在"}))
            return False
        if get_captcha.response == captchaStr.lower (): # 不区分大小写
            return True
        else:
            # return HttpResponse (json.dumps ({'code': 4402, "info": "验证码错误"}))
            return False
    else:
        # return HttpResponse (json.dumps ({'code': 4403, "info": "验证码输入/hashkey缺失"}))
        return False
