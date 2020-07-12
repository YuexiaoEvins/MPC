from django.utils.datetime_safe import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from Tool.decorator import check_request
from article.dao.ArticleDao import query_point_count

from article.models import Article, Collection, Record


from users.utils.token_op import get_userid, checkToken


# 文章收藏功能
@csrf_exempt
@check_request('article_id', 'token')
@checkToken ("")
def collecteArticle(request):
    try:
        json_req = json.loads(request.body)
        article_id = json_req['article_id']
        user_id = get_userid(json_req['token'])  # 当前用户
        # 先查询是否已经存在收藏记录
        collection = Collection.objects.filter(user_id=user_id, article_id=article_id)
        # 收藏记录已经存在取反后返回
        if collection.exists():
            flag = Collection.objects.get(user_id=user_id, article_id=article_id).flag
            if flag == 0:
                collection.update(create_time=datetime.now(), flag=1)
                return HttpResponse(json.dumps({'code': 200, 'collect_flag': 1}, ensure_ascii=False),
                                    content_type="application/json")
            if flag == 1:
                collection.update(create_time=datetime.now(), flag=0)
                return HttpResponse(json.dumps({'code': 200, 'collect_flag': 0}, ensure_ascii=False),
                                    content_type="application/json")
        else:
            collection = Collection(article_id=article_id, user_id=user_id, create_time=datetime.now(), flag=1)
            collection.save()
            return HttpResponse(json.dumps({'code': 200, 'collect_flag': 1}, ensure_ascii=False),
                                content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 文章点赞功能
@csrf_exempt
@check_request('article_id', 'token')
@checkToken ("")
def pointArticle(request):
    json_req = json.loads(request.body)
    article_id = json_req['article_id']
    user_id = get_userid(json_req['token'])  # 当前用户
    # 先查询是否已经存在点赞记录
    record = Record.objects.filter(user_id=user_id, article_id=article_id)
    conn = get_redis_connection('default')
    point_count = query_point_count(article_id)  # 在redis中获取文章的点赞量
    if record.exists():  # 点赞已经存在取反后返回
        flag = Record.objects.get(user_id=user_id, article_id=article_id).flag
        if flag == 0:  # 原本为未点赞状态，点击后为用户点赞，
            record.update(create_time=datetime.now(), flag=1)
            Article.objects.filter(article_id=article_id).update(point_count=point_count + 1)  # DB中点赞数要加一
            conn.hset('article_point_count', article_id, point_count + 1)  # 缓存中点赞数加一
            return HttpResponse(
                json.dumps({'code': 200, 'point_count': point_count + 1, 'point_flag': 1}, ensure_ascii=False),
                content_type="application/json")
        if flag == 1:  # 原本为点赞状态，用户取消点赞，点赞数要减一
            record.update(create_time=datetime.now(), flag=0)
            Article.objects.filter(article_id=article_id).update(point_count=point_count - 1)
            conn.hset('article_point_count', article_id, point_count - 1)
            return HttpResponse(
                json.dumps({'code': 200, 'point_count': point_count - 1, 'point_flag': 0}, ensure_ascii=False),
                content_type="application/json")
    # 点赞记录不存在时，则创建记录
    else:
        record = Record(article_id=article_id, user_id=user_id, create_time=datetime.now(), flag=1)
        record.save()
        Article.objects.filter(article_id=article_id).update(point_count=point_count + 1)
        conn.hset('article_point_count', article_id, point_count + 1)
        return HttpResponse(
            json.dumps({'code': 200, 'point_count': point_count + 1, 'point_flag': 1}, ensure_ascii=False),
            content_type="application/json")

