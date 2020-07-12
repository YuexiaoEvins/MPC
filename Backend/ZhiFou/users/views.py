# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, request, HttpResponse

from article.dao.ArticleDao import getLevelName,getCollecteArticleCount,getUserWriteCount,queryPointByUserId


from .utils.token_op import checkToken
from .models import User
from .utils import token_op
from .forms import UserForm, RegisterForm
from django.conf import settings
import json
import os
import datetime
import uuid


# ##register_User
# 注册
# user_account 用户账号
# user_name 用户名
# password 用户密码
# 返回JSON数据
# code           状态码 200成功, . 401用户账号已存在 404请求方式错误
@csrf_exempt
def register_User(request):
    if request.method == "POST":
        reg_user_info = json.loads ((request.body))
        user_account = reg_user_info['user_account']
        password = reg_user_info['password']
        email = reg_user_info['email']
        user_name = reg_user_info['user_name']
        is_Exist_user = User.objects.filter (user_account=user_account)
        if len (is_Exist_user):
            return HttpResponse (json.dumps ({"code": 401}))
        User.objects.create_user (  # 调用class userManager的方法
            user_account=user_account,
            user_name=user_name,
            email=email,
            password=password,
        )
        test_user = User.objects.get(user_account=user_account)
        test_user.save()
        return HttpResponse (json.dumps ({"code": 200}))

        #     #待定功能：邮箱验证
    return HttpResponse (json.dumps ({"code": 404}))




# 测试验证token的装饰器使用
# url:/users/viewDemo
# 需求参数：token+user_id
# 参数类型：JSON
@csrf_exempt
@checkToken ("")
def viewDemo(request):
    if request.method == 'POST':
        json_req = json.loads (request.body)
        user_id = json_req['user_id']
        try:
            user = User.objects.get (user_id=user_id)
            return HttpResponse (json.dumps ({
                'code': 200,
                'user_id': user.user_id,
                'user_account': user.user_account,
                'user_url': user.user_url,
                'user_name': user.user_name,
                'user_gender': user.user_gender,
                'email': user.email,
                'user_phone': user.user_phone,
                'user_credit': user.user_credit
            }))
        except:
            return HttpResponse (json.dumps ({'code': 404}))  # 用户信息查看失败，user_id可能不存在
    else:
        return HttpResponse (json.dumps ({'code': 402}))  # 请求方式错误


###view_UserInfo
# 查看用户信息功能
# 以user_id作为查询条件
# 返回JSON数据
# code           状态码 200成功 404用户不存在  401token错误  402请求方式错误
# user_name      用户名
# user_url       头像链接
# user_gender    性别
# email          电子邮箱
# user_phone     电话
# user_credit    积分
@csrf_exempt
def view_UserInfo(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['user_id']
            token = request.POST['token']
            user = User.objects.get (user_id=user_id)
        except:
            return HttpResponse (json.dumps ({'code': 404}))  # 用户信息查看失败，user_id可能不存在，或表单错误 
        if token_op.check_token (token):
            return HttpResponse (json.dumps ({
                'code': 200,
                'user':{
                    'user_account': user.user_account,
                    'user_id':user.user_id,
                    'user_url': add_address_profile_url(user.user_url),
                    'user_name': user.user_name,
                    'user_gender': user.user_gender,
                    'email': user.email,
                    'user_phone': user.user_phone,
                    'user_credit': user.user_credit,

                }
            }))
        else:
            return HttpResponse (json.dumps ({'code': 401}))  # token不存在
    else:
        return HttpResponse (json.dumps ({'code': 402}))  # 请求方式错误

#接收json格式数据
#查看用户信息
@csrf_exempt
def view_UserInfo_json(request):
    if request.method == 'POST':
        try:
            user_info = json.loads(request.body)
            user_id = user_info['user_id']
            token = user_info['token']
            user = User.objects.get (user_id=user_id)
        except:
            return HttpResponse (json.dumps ({'code': 404}))  # 用户信息查看失败，user_id可能不存在，或表单错误 
        if token_op.check_token (token):
            return HttpResponse (json.dumps ({
                'code': 200,
                'user':{
                    'user_account': user.user_account,
                    'user_id':user.user_id,
                    'user_url': add_address_profile_url(user.user_url),
                    'user_name': user.user_name,
                    'user_gender': user.user_gender,
                    'email': user.email,
                    'user_phone': user.user_phone,
                    'user_credit': user.user_credit,

                    'user_write_count':getUserWriteCount(user.user_id),
                    'user_collect_count':getCollecteArticleCount(user.user_id),
                    'user_point':queryPointByUserId(user.user_id),
                    'user_level_name':getLevelName(write_count=getUserWriteCount(user.user_id),point_count=queryPointByUserId(user.user_id)),

                }
            }),content_type="application/json")
        else:
            return HttpResponse (json.dumps ({'code': 401}))  # token不存在
    else:
        return HttpResponse (json.dumps ({'code': 402}))  # 请求方式错误    

###update_UserInfo
# 更新用户信息功能
# 接收表单数据，更新所有信息
# 以user_account作为查询条件
# 暂不实现安全验证功能
# 状态码 200成功 404用户不存在  401token错误  402请求方式错误 403token与user_id不匹配
@csrf_exempt
def update_UserInfo(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['user_id']
            token = request.POST['token']
            if token_op.check_token (token):
                if str (token_op.get_userid (token)) == str(user_id):
                    user = User.objects.get (user_id=user_id)
                    user.user_name = request.POST['user_name']
                    user.user_url = get_profile_filename(request.POST['user_url'])
                    user.user_gender = request.POST['user_gender']
                    user.email = request.POST['email']
                    user.user_phone = request.POST['user_phone']
                    user.save ()
                    # User.objects.filter(user_id = user_id).update(user_url=user.url)
                    return HttpResponse (json.dumps ({'code': 200}))
                else:
                    return HttpResponse (json.dumps ({'code': 403}))  # token与user_id不匹配
            else:
                return HttpResponse (json.dumps ({'code': 401}))  # token不存在
        except:
            return HttpResponse (json.dumps ({'code': 404}))  # 用户信息修改失败，user_id可能不存在或表单错误


@csrf_exempt
def update_UserInfo_json(request):
    if request.method == 'POST':
        try:
            user_info = json.loads ((request.body))
            user_id = user_info['user_id']
            token = user_info['token']
            if token_op.check_token (token):
                if str (token_op.get_userid (token)) == str(user_id) :
                    user = User.objects.get (user_id=user_id)
                    user.user_name = user_info['user_name']
                    user.user_url = get_profile_filename(user_info['user_url'])
                    user.user_gender = user_info['user_gender']
                    user.email = user_info['email']
                    user.user_phone = user_info['user_phone']
                    user.save()
                    return HttpResponse (json.dumps ({'code': 200}))
                else:
                    return HttpResponse (json.dumps ({'code': 403}))  # token与user_id不匹配
            else:
                return HttpResponse (json.dumps ({'code': 401}))  # token不存在
        except:
            return HttpResponse (json.dumps ({'code': 404}))  # 用户信息修改失败，user_id可能不存在或表单错误

@csrf_exempt
def update_UserInfo_demo(request):
    if request.method == 'POST':
        try:
            user_info = json.loads ((request.body))
            user_id = user_info['user_id']
            token = user_info['token']
            if token_op.check_token (token):
                if str (token_op.get_userid (token)) == str(user_id):
                    user = User.objects.get (user_id=user_id)
                    user.user_url = get_profile_filename(user_info['user_url'])
                    user.save()
                    return HttpResponse(json.dumps ({'code': 200}))
                else:
                    return HttpResponse(json.dumps ({'code': 403}))  # token与user_id不匹配
            else:
                return HttpResponse(json.dumps ({'code': 401}))  # token不存在
        except:
            return HttpResponse(json.dumps ({'code': 404}))  # 用户信息修改失败，user_id可能不存在或表单错误

# POST请求
# 上传图片,并返回url 暂为文件名
@csrf_exempt
def upload_files(request):
    if request.method == "POST":
        try:
            user_id = request.POST['user_id']
            token = request.POST['token']
            file = request.FILES['profile_photo']
        except:
            return HttpResponse (json.dumps ({"code": 404,"information":"表单错误"}), content_type="application/json")  # 上传失败，可能为表单错误
        
        if str (token_op.get_userid (token)) == str(user_id):
            if file.name.split ('.')[-1] not in ['jpeg', 'jpg', 'png', 'JPEG', 'JPG', 'PNG']:
                return HttpResponse (json.dumps ({'code': 405,"information":"上传格式错误"}))  # 上传格式错误

            filename = str(user_id)+'_'+ str (uuid.uuid1 ()) + '.' + file.name.split (".")[-1]
            url = get_profile_url(filename)
            filepath = os.path.join (settings.MEDIA_ROOT, 'profile', filename)
            with open (filepath, 'wb') as f:
                for chunk in file.chunks ():
                    f.write (chunk)
            return HttpResponse (json.dumps ({"code": 200, "url": url}), content_type="application/json")
        else:
            return HttpResponse (json.dumps ({'code': 403}))  # token与user_id不匹配



# 该函数用于测试服务器访问图片是否正常
def demo_image(request):
    d = settings.MEDIA_ROOT
    # print("d="+str(d))
    imagepath = os.path.join (d, 'profile', "test.jpg")
    # print("imagepath="+str(imagepath))
    image_data = open (imagepath, "rb").read ()
    return HttpResponse (image_data, content_type="image/png")

#已弃用
# 输入url 即文件名，读取MEDIA_ROOT下对应的文件，返回图像数据 
def get_image_data(url):
    filepath = os.path.join (settings.MEDIA_ROOT, 'profile', url)
    with open (filepath, "rb") as file:
        imagedata = file.read ()
    return imagedata

# 已弃用
###GET请求 
# 请求参数 user_url
# 返回对应图片
def get_profile_photo(request, url):
    imagedata = get_image_data (url)
    return HttpResponse (imagedata, content_type="image/png")

#拼接文件名，返回图片请求链接 eg. name.jpg  ->  http://ip:port/static/profile/name.jpg
def get_profile_url(filename):
    url = settings.SERVER_ADDRESS +'/static/profile/' + filename 
    return url

#拼接文件名，返回图片请求链接 eg. /static/profile/name.jpg  ->  http://ip:port/static/profile/name.jpg
def add_address_profile_url(filename):
    url = settings.SERVER_ADDRESS + filename 
    return url

#拆分图片请求链接，获取文件名后拼接  eg. http://ip:port/static/profile/name.jpg  ->  /static/profile/name.jpg
def get_profile_filename(url):
    return  '/static/profile/' + url.split('/')[-1]