#import users

from django.urls import path, include

from users.view import loginView, passwdView, emailView, captchaView, tokenView
from users import views
from users.searchUser import UserSearchView


urlpatterns = [
    # 用户搜索
    path('search',UserSearchView()),

    path('info',views.view_UserInfo),
    path('info_json',views.view_UserInfo_json),
    path('update',views.update_UserInfo),
    path('image',views.demo_image),
    path('profile/<str:url>',views.get_profile_photo),
    path('uploadfiles',views.upload_files),
    path('update_json',views.update_UserInfo_json),
    path('updatedemo',views.update_UserInfo_demo),

    # 用户登录
    path ('login', loginView.login),        # json数据登录
    path ('logindemo', loginView.login_demo),  # 登录，带验证码

    # 用户注册
    path ('reg', views.register_User),
    # path ('reg_demo', views.register_User2),

    path ('viewDemo', views.viewDemo),

    # 修改密码
    path('resetpasswd', passwdView.reset_password),     # 登录状态下修改密码
    path ('forgetpasswd', emailView.send_email_reset_password),  # 邮件链接重置密码
    path ('changepasswd', passwdView.reset_password_by_email), # 发送邮件找回密码

    # 验证码
    path ('captcha', include ('captcha.urls')),
    path('getcaptcha',captchaView.get_captcha), # 获取验证码
    path('checktoken',tokenView.check_token_validity),
]