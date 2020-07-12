import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request, check_order, toIp
from Tool.page_tool import PageInfo
from article.dao.ArticleDao import getTypeName, queryPoint, queryUserInfo, queryPhotoInfo, getUserWriteCount, \
    query_page_view, up_page_view, queryCollect, queryPointByUserId, getLevelName, \
    getCollecteArticleCount, query_point_count

from article.models import Collection, Article

from comment.dao.CommentDao import getArticleCommentCount
from users.utils.token_op import get_userid, checkToken


# 首页查询
@csrf_exempt
@check_request('page', 'order_type', 'token')
@checkToken("")
def queryArticle(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])  # 当前用户
        order = check_order(json_req['order_type'])  # 排序类型默认按时间，0 按时间，1 按阅读数，2 按点赞数
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 10)
        article_count = Article.objects.filter(flag=1).count()  # 有效文章的总数量
        articles = Article.objects.filter(flag=1).order_by(order)[page_info.start():page_info.end()]
        json_list = []
        for article in articles:
            json_dict = {"article_id": article.article_id,
                         "title": article.title,
                         "simple_content": article.simple_content,
                         "page_view": query_page_view(article.article_id),
                         "create_time": article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "type_id": article.type_id,
                         "type_name": getTypeName(article.type_id),
                         "point_count": query_point_count(article.article_id),
                         "point_flag": queryPoint(user_id, article.article_id),
                         "collect_flag": queryCollect(user_id, article.article_id),
                         "user": queryUserInfo(article.user_id.user_id),
                         "photo": queryPhotoInfo(article.article_id),
                         "comment_count": getArticleCommentCount(article.article_id),
                         "level_name": getLevelName(getUserWriteCount(article.user_id.user_id), queryPointByUserId(article.user_id.user_id))  # 作者获得的称号
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}, ensure_ascii=False), content_type="application/json")


# 查看文章详情 12.17
@csrf_exempt
@check_request('article_id', 'token')
@checkToken ("")
def queryArticleDetailed(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])  # 当前用户
        article_id = json_req['article_id']
        up_page_view(article_id)  # 再redis中将阅读数加一
        article = Article.objects.get(article_id=article_id)
        collection_count = Collection.objects.filter(article_id=article_id).count()  # 该文章已被多少人收藏
        write_count = getUserWriteCount(article.user_id.user_id)
        user_point_count = queryPointByUserId(article.user_id.user_id)
        json_dict = {"article_id": article.article_id,
                     "title": article.title,
                     "content": article.content,
                     "page_view": query_page_view(article.article_id),
                     "create_time": article.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                     "point_count": query_point_count(article.article_id),
                     "type_id": article.type_id,
                     "type_name": getTypeName(article.type_id),
                     "point_flag": queryPoint(user_id, article.article_id),
                     "collect_flag": queryCollect(user_id, article.article_id),  # 登录用户是否收藏该文章
                     "user_point_count": user_point_count,  # 获取该文章的作者共获得多少赞
                     "user": queryUserInfo(article.user_id.user_id),   # 获取作者基本信息
                     "comment_count": getArticleCommentCount(article.article_id),  # 该文章有多少条评论
                     "write_count": write_count,
                     "collection_count": collection_count,
                     "level_name": getLevelName(write_count, user_point_count)  # 作者获得的称号
                     }
        result = {'code': 200, 'article': json_dict}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}, ensure_ascii=False), content_type="application/json")


# 分类查询
@csrf_exempt
@check_request('page', 'type_id', 'order_type', 'token')
@checkToken ("")
def queryArticleByTypeId(request):
    try:
        json_req = json.loads(request.body)
        type_id = json_req['type_id']
        user_id = get_userid(json_req['token'])
        order = check_order(json_req['order_type'])  # 排序类型默认按时间，0 按时间，1 按阅读数，2 按点赞数
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 10)
        article_count = Article.objects.filter(type_id=type_id, flag=1).count()
        articles = Article.objects.filter(type_id=type_id, flag=1).order_by(order)[page_info.start():page_info.end()]
        json_list = []
        for article in articles:
            json_dict = {"article_id": article.article_id,
                         "title": article.title,
                         "simple_content": article.simple_content,
                         "page_view": query_page_view(article.article_id),
                         "create_time": article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "point_count": query_point_count(article.article_id),
                         "user": queryUserInfo(article.user_id.user_id),
                         "point_flag": queryPoint(user_id, article.article_id),
                         "photo": queryPhotoInfo(article.article_id),
                         "comment_count": getArticleCommentCount(article.article_id),
                         "level_name": getLevelName(getUserWriteCount(article.user_id.user_id), queryPointByUserId(article.user_id.user_id))  # 作者获得的称号
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}, ensure_ascii=False), content_type="application/json")


# 阅读全文
@csrf_exempt
@check_request('article_id', 'token')
@checkToken ("")
def readFullArticle(request):
    try:
        json_req = json.loads(request.body)
        article_id = json_req['article_id']
        up_page_view(article_id)  # 再redis中将阅读数加一
        content = Article.objects.get(article_id=article_id).content
        result = {'code': 200, 'content': content}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}, ensure_ascii=False), content_type="application/json")


# 获取首页的轮播图片地址
@csrf_exempt
def getIndexPhoto(request):
    advertise = [
        toIp() + '/static/default/advertise1.jpg',
        toIp() + '/static/default/advertise2.jpg',
        toIp() + '/static/default/advertise3.jpg'
    ]
    result = {'code': 200, 'advertise': advertise}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
