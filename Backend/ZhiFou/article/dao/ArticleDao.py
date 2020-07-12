import json

from django.db.models import Sum
from django.http import HttpResponse
from django_redis import get_redis_connection

from Tool.decorator import toIp

from article.models import Article, Type, User, Photo, Record, Collection


# 在redis中获取文章的点赞量 先读取缓存的，缓存不存在再读取db的
def query_point_count(article_id):
    try:
        conn = get_redis_connection('default')
        # 先获取key是否存在
        count = conn.hget('article_point_count', article_id)
        # redis不存在该文章的点赞量,则查询数据库数据，然后放进redis
        if count is None:
            point_count = Article.objects.get(article_id=article_id).point_count
            conn.hset('article_point_count', article_id, point_count)
            return point_count
        # redis存在文章的浏览量，则直接返回
        point_count = int(count.decode('utf-8'))
        return point_count
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 阅读数加一 写入操作：先写入DB然后写入缓存
# 阅读全文和查看文章详情功能执行后执行
def up_page_view(article_id):
    try:
        page_view = Article.objects.get(article_id=article_id).page_view + 1
        Article.objects.filter(article_id=article_id).update(page_view=page_view)
        conn = get_redis_connection('default')
        conn.hset('article_page_view', article_id, page_view)
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 在redis中获取文章的阅读数 先读取缓存的，缓存不存在再读取db的
def query_page_view(article_id):
    try:
        conn = get_redis_connection('default')
        # 先获取key是否存在
        count = conn.hget('article_page_view', article_id)
        # redis不存在该文章的浏览量,则查询数据库数据，然后放进redis
        if count is None:
            point_count = Article.objects.get(article_id=article_id).point_count
            conn.hset('article_page_view', article_id, point_count)
            return point_count
        # redis存在文章的浏览量，则直接返回
        page_view = int(count.decode('utf-8'))
        return page_view
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 获取文章所属图片的url及其flag
# article_id  文章ID号
def queryPhotoInfo(article_id):
    photo = list(Photo.objects.filter(article_id=article_id, flag__in=[3, 0]).values("photo_url", "flag").order_by("-flag")[0:1])
    if photo == []:
        return dict(photo)
    json_dict = {
        "photo_url": toIp() + photo[0]['photo_url'],  # 拼接上服务器地址端口
        "photo_flag": photo[0]['flag']
    }
    return json_dict


# 获取文章关联的用户信息
def queryUserInfo(user_id):
    user = list(User.objects.filter(user_id=user_id).values("user_id", "user_account", "user_name", "user_url", "user_credit" ))
    if user == []:
        return dict(user)
    json_dict = {
        "user_id": user[0]['user_id'],
        "user_account": user[0]['user_account'],
        "user_name": user[0]['user_name'],
        "user_url": toIp() + user[0]['user_url'],  # 拼接上服务器地址端口
        "user_credit": user[0]['user_credit']
    }
    return json_dict


# 根据分类id获取分类名
def getTypeName(type_id):
    try:
        type_name = Type.objects.get(type_id=type_id).type_name
        return type_name
    except:
        return Type.objects.get(type_id=1009).type_name  # 分类id归并为生活


# 查看用户是否对该文章点过赞
def queryPoint(user_id, article_id):
    try:
        point_flag = Record.objects.get(article_id=article_id, user_id=user_id).flag
        return point_flag
    except:
        return 0  # 如果没有查到该记录则返回零


# 查看用户是否收藏过该文章
def queryCollect(user_id, article_id):
    try:
        collect_flag = Collection.objects.get(article_id=article_id, user_id=user_id).flag
        return collect_flag
    except:
        return 0  # 如果没有查到该记录则返回零


# 根据article_id获取文章的信息
def queryArticleByArticleId(article_id):
    article = list(Article.objects.filter(article_id=article_id).values("article_id", "user_id", "title", "simple_content", "create_time", "type_id"))
    print(article)
    if article == []:
        return dict(article)
    json_dict = {
        "article_id": article[0]['article_id'],
        "title": article[0]['title'],
        "simple_content": article[0]['simple_content'],
        "page_view": query_page_view(article[0]['article_id']),
        "create_time": article[0]['create_time'].strftime("%Y-%m-%d %H:%M:%S"),
        "type_id": article[0]['type_id'],
        "type_name": getTypeName(article[0]['type_id']),
        "point_count": query_point_count(article[0]['article_id']),
        "user": queryUserInfo(article[0]['user_id'])
    }
    return json_dict


# 根据用户id获取用户的共获得的点赞数量
def queryPointByUserId(user_id):
    try:
        user_point_count = Article.objects.filter(user_id=user_id, flag=1).aggregate(Sum('point_count'))
        if user_point_count['point_count__sum'] is None:
            return 0 # 如果没有查到该记录则返回零
        return user_point_count['point_count__sum']
    except:
        return 0


# 用户发表过多少篇文章
def getUserWriteCount(user_id):
    try:
        count = Article.objects.filter(user_id=user_id).count()  # 该用户发表过多少篇文章
        return count
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 查看用户收藏过多少篇文章
def getCollecteArticleCount(user_id):
    try:
        count = Collection.objects.filter(user_id=user_id).count()  # 该用户发表过多少篇文章
        return count
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 根据作者的已发文章量和共获得的点赞量给予称号
def getLevelName(write_count, point_count):
    level_name = '倔强青铜'
    if write_count > 5 and point_count > 50:
        level_name = '秩序白银'
        if write_count > 15 and point_count > 300:
            level_name = '荣耀黄金'
            if write_count > 25 and point_count > 500:
                level_name = '尊贵铂金'
                if write_count > 35 and point_count > 700:
                    level_name = '永恒钻石'
                    if write_count > 45 and point_count > 900:
                        level_name = '至尊星耀'
                        if write_count > 55 and point_count > 1100:
                            level_name = '最强王者'
    return level_name