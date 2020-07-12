import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request
from Tool.page_tool import PageInfo
from article.dao.ArticleDao import getTypeName, queryPoint, queryPhotoInfo, \
    query_page_view, queryArticleByArticleId, queryCollect, queryUserInfo

from article.models import Collection, Article, Comment, Record
from comment.dao.CommentDao import getArticleCommentCount
from reply.dao.replyDao import query_reply_count

from users.utils.token_op import get_userid, checkToken


# 用户已发帖子
@csrf_exempt
@check_request('user_id', 'page', 'token')
@checkToken ("")
def queryArticleByMyself(request):
    try:
        json_req = json.loads(request.body)
        user_id = json_req['user_id']
        login_user_id = get_userid(json_req['token'])  # 当前登录用户的user_id
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 10)
        article_count = Article.objects.filter(user_id=user_id, flag=1).count()
        articles = Article.objects.filter(user_id=user_id, flag=1).order_by("-create_time")[page_info.start():page_info.end()]
        json_list = []
        for article in articles:
            json_dict = {"article_id": article.article_id,
                         "title": article.title,
                         "simple_content": article.simple_content,
                         "page_view": query_page_view(article.article_id),
                         "create_time": article.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                         "point_count": article.point_count,
                         "type_id": article.type_id,
                         "type_name": getTypeName(article.type_id),
                         "point_flag": queryPoint(login_user_id, article.article_id),
                         "collect_flag": queryCollect(login_user_id, article.article_id),
                         "user": queryUserInfo(article.user_id.user_id),
                         "photo": queryPhotoInfo(article.article_id),
                         "comment_count": getArticleCommentCount(article.article_id),
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 用户已收藏文章
@csrf_exempt
@check_request('page', 'token')
@checkToken ("")
def queryCollectionByUserId(request):
    try:
        json_req = json.loads(request.body)
        login_user_id = get_userid(json_req['token'])
        article_count = Collection.objects.filter(user_id=login_user_id, flag=1).count()  # 获取该用户已收藏文章的数量
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 10)
        collects = list(Collection.objects.filter(user_id=login_user_id, flag=1).values('article_id').order_by("-create_time")[page_info.start():page_info.end()])
        json_list = []
        for collect in collects:
            json_dict = {
                         "article": queryArticleByArticleId(collect['article_id']),
                         "point_flag": queryPoint(login_user_id, collect['article_id']),
                         "collect_flag": queryCollect(login_user_id, collect['article_id']),
                         "photo": queryPhotoInfo(collect['article_id']),
                         "comment_count": getArticleCommentCount(collect['article_id']),
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'data': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 查询用户已评论文章
@csrf_exempt
@check_request('page', 'user_id', 'token')
@checkToken ("")
def queryCommentByUserId(request):
    json_req = json.loads(request.body)
    user_id = json_req['user_id']
    login_user_id = get_userid(json_req['token'])  # 当前登录用户的user_id
    article_count = Comment.objects.filter(user_id=user_id, is_delete=1).count()  # 用户评论过的文章 数量
    page = json_req['page']
    # 分页查询文章信息
    page_info = PageInfo(page, 10)
    comments = list(Comment.objects.filter(user_id=user_id, is_delete=1).values('comment_id', 'article_id', 'comment_content', 'create_time').order_by("-create_time")[page_info.start():page_info.end()])
    json_list = []
    for comment in comments:
        json_dict = {"comment_id": comment['comment_id'],
                     "reply_count": query_reply_count(comment['comment_id']),
                     "comment_content": comment['comment_content'],
                     "comment_create_time": comment['create_time'].strftime("%Y-%m-%d %H:%M:%S"),
                     "article": queryArticleByArticleId(comment['article_id']),
                     "point_flag": queryPoint(login_user_id, comment['article_id']),
                     "collect_flag": queryCollect(login_user_id, comment['article_id']),
                     "photo": queryPhotoInfo(comment['article_id']),
                     "comment_count": getArticleCommentCount(comment['article_id'])
                     }
        json_list.append(json_dict)
    result = {'code': 200, 'article_count': article_count, 'data': json_list}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")



# 查询用户已点赞文章
@csrf_exempt
@check_request('page', 'user_id', 'token')
@checkToken ("")
def queryPointByUserId(request):
    json_req = json.loads(request.body)
    user_id = json_req['user_id']
    login_user_id = get_userid(json_req['token'])  # 当前登录用户的user_id
    article_count = Record.objects.filter(user_id=user_id, flag=1).count()  # 用户点赞过的文章数量
    page = json_req['page']
    # 分页查询文章信息
    page_info = PageInfo(page, 10)
    records = list(Record.objects.filter(user_id=user_id, flag=1).values('article_id', 'create_time').order_by("-create_time")[page_info.start():page_info.end()])
    json_list = []
    for record in records:
        json_dict = {
                     "point_create_time": record['create_time'].strftime("%Y-%m-%d %H:%M:%S"),  # 点赞时间
                     "article": queryArticleByArticleId(record['article_id']),
                     "point_flag": queryPoint(login_user_id, record['article_id']),
                     "collect_flag": queryCollect(login_user_id, record['article_id']),
                     "photo": queryPhotoInfo(record['article_id']),
                     "comment_count": getArticleCommentCount(record['article_id']),
                     }
        json_list.append(json_dict)
    result = {'code': 200, 'article_count': article_count, 'data': json_list}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    
