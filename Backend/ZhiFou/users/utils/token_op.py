import json
import time
import hashlib  # 涉及安全散列和消息摘要，提供多个不同的加密算法接口，eg：sha256，md5……
from django.core import signing  # django内置模块，加密解密任何数据
from django.core.cache import cache
from django.http import HttpResponse

# 使用signing
HEADER = {'typ': 'JWT', 'alg': 'default'}
KEY = 'ZhiFou'
SALT = 'django.core.signing'
TIME_OUT = 60 * 60 * 24 * 7 # 过期时间 7天


def encrypt(obj):
    """加密"""
    value = signing.dumps (obj, key=KEY, salt=SALT)
    value = signing.b64_encode (value.encode ()).decode ()
    return value


def decrypt(obj):
    """解密"""
    src = signing.b64_decode (obj.encode ()).decode ()
    raw = signing.loads (src, key=KEY, salt=SALT)
    return raw


# 登录后生成token返回
def create_token(user):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt (HEADER)
    # 2. 构造Payload:用户id+用户名+密码+发行时间
    payload = {"id": user.user_id, "username": user.user_account, "password": user.password, "iat": time.time ()}
    payload = encrypt (payload)
    # 3. 生成签名
    # md5 = hashlib.md5 ()
    # md5.update (("%s.%s" % (header, payload)).encode ())
    # signature = md5.hexdigest ()
    # token = "%s.%s.%s" % (header, payload, signature)  # 用.分割三部分
    token = packing_token (header, payload)
    # 存储到缓存中
    cache.set (user.user_id, token, TIME_OUT)
    return token

# 包装token三部分部分
# 返回token
def packing_token(header, payload):
    # 3. 生成签名
    md5 = hashlib.md5 ()
    md5.update (("%s.%s" % (header, payload)).encode ())
    signature = md5.hexdigest ()
    token = "%s.%s.%s" % (header, payload, signature)  # 用.分割三部分
    return token


# 获取token的信息主体
def get_payload(token):
    payload = str (token).split ('.')[1]
    payload = decrypt (payload)
    return payload


# 通过token获取用户名
def get_username(token):
    payload = get_payload (token)
    return payload['username']
    pass


# 通过token获取用户名
def get_email(token):
    payload = get_payload (token)
    return payload['email']
    pass


# 通过token获取用户id
def get_userid(token):
    payload = get_payload (token)
    return payload['id']


# 通过token获取用户密码
def get_password(token):
    payload = get_payload (token)
    return payload['password']

# 验证token是否存在并一致
def check_token(token):
    try:
        user_id = get_userid (token)  # 解析传入token，获取token串对应的user_id
    except:
        return False
    last_token = cache.get (user_id)  # 查redis内对应user_id的token
    if last_token == token:  # 判断传入token是否等于redis内token
        return True
    return False


# 装饰器，验证token
# （1）check_token:解析token，获取token包装信息的user_id，并比较此token和id对应redis的token是否相同
# （2）校验传入的user_id和token包装信息user_id是否一致,防止盗用token
def checkToken(param):
    def __checkToken(func):
        def warpper(request):
            try:
                json_req = json.loads(request.body)
                token = json_req['token']
                # user_id = json_req['user_id']
            except:
                return HttpResponse(
                    json.dumps({'code': '4401', 'info': '获取不到参数token'}))  # 获取不到参数token/user_id
            if check_token(token):  # 验证token
                # if get_userid (token) == user_id:
                #     return func (request)  # 验证通过，继续执行后续
                # else:
                #     return HttpResponse (
                #         json.dumps ({'code': '4402', 'info': '实际用户id与token的id不匹配'}))  # 实际用户id与token的id不匹配
                return func(request)
            else:
                return HttpResponse(json.dumps ({'code': '4403', 'info': 'token无法解析/验证失败'}))  # token无法解析/验证失败
        return warpper
    return __checkToken


# 忘记密码，邮件找回的token
def create_email_token(user):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt (HEADER)
    # 2. 构造Payload:用户id+用户名+密码+发行时间
    payload = {"id": user.user_id, "email": user.email, "iat": time.time ()}
    payload = encrypt (payload)
    # 3.生成签名并返回token
    token = packing_token (header, payload)
    # 存储到缓存中
    cache.set (user.email, token, TIME_OUT)
    return token
