


import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request
from Tool.page_tool import PageInfo
from article.dao.ArticleDao import getTypeName, queryPhotoInfo
from article.models import Article



# 查看草稿箱信息
from users.utils.token_op import get_userid, checkToken


@csrf_exempt
@check_request('page')
@checkToken ("")
def queryDraftBox(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 10)
        article_count = Article.objects.filter(user_id=user_id,flag=0).count()
        articles = Article.objects.filter(user_id=user_id,flag=0).order_by("-create_time")[page_info.start():page_info.end()]
        json_list = []
        for article in articles:
            json_dict = {"article_id": article.article_id,
                         "title": article.title,
                         "simple_content": article.simple_content,
                         "page_view": article.page_view,
                         "create_time": article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "type_id": article.type_id,
                         "type_name": getTypeName(article.type_id),
                         "photo": queryPhotoInfo(article.article_id)
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 编辑草稿
@csrf_exempt
@check_request('article_id')
@checkToken ("")
def editorDraftBox(request):
    try:
        json_req = json.loads(request.body)
        article_id = json_req['article_id']
        article = Article.objects.get(article_id=article_id, flag=0)
        json_list = []
        json_dict = {"article_id": article.article_id,
                     "title": article.title,
                     "content": article.content,
                     "type_id": article.type_id,
                     "type_name": getTypeName(article.type_id)
                     }
        json_list.append(json_dict)
        result = {'code': 200, 'comment': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")

