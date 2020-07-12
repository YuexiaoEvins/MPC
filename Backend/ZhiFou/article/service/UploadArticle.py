import json
import re
from builtins import len

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request

from article.models import Article, User


# 保存文章（发表文章或者保存草稿）
from users.utils.token_op import get_userid, checkToken


@csrf_exempt
@check_request('article_id', 'title', 'content', 'type_id', 'flag', 'token')
@checkToken ("")
def saveArticle(request):
    json_req = json.loads(request.body)
    article_id = json_req['article_id']
    title = json_req['title']
    type_id = json_req['type_id']
    flag = json_req['flag']
    content = json_req['content']
    user_id = get_userid(json_req['token'])
    try:
        if type_id < 1001 or type_id > 1009:
            return HttpResponse(json.dumps({'code': 405, 'information': '参数异常！'}), content_type="application/json")
        if len(title) > 30:
            result = {'code': 406, 'information': '字数超过限制！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        dr = re.compile(r'<[^>]+>', re.S)
        filter_content = dr.sub('', content)
        tag = {
           '&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>',
           '&apos;': "'", '&nbsp;': ' ', '&yen;': '¥', '&copy;': '©', '&divide;': '÷',
           '&hellip;': '…', '&times;': '×','&middot;': '·',
            }
        for k, v in tag.items():
            filter_content = filter_content.replace(k, v)   # 除去html里面的常用实体字符
        login_user = User.objects.get(user_id=user_id)
        # 获得过滤标签后filter_content的字数
        a = len(filter_content)
        # content的字数大于100则截取作为简介，否则就直接作为简介存储
        if a > 100:
            simple_content = filter_content[0:100]
        else:
            simple_content = filter_content
        # flag=1,发布文章
        if flag == 1:
            # 发表文章
            article = Article(article_id=article_id, user_id=login_user, title=title, simple_content=simple_content,content=content,type_id=type_id, flag=1)
            article.save()
            # 积分+5
            login_user.user_credit = login_user.user_credit+5
            login_user.save()
        # flag=0,保存草稿
        else:
            article = Article(article_id=article_id, user_id=login_user,title=title, simple_content=simple_content,content=content,type_id=type_id, flag=0)
            article.save()
        result = {'code': 200}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}), content_type="application/json")


# 删除文章或者草稿
@csrf_exempt
@check_request('article_id')
@checkToken ("")
def delArticleOrDraft(request):
    json_req = json.loads(request.body)
    article_id = json_req['article_id']
    try:
        article = Article.objects.filter(article_id=article_id).update(flag=2)
        if article > 0:
            result = {'code': 200}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")



# 生成文章ID
@csrf_exempt
@check_request('type_id','token')
@checkToken ("")
def createArticleId(request):
    try:
        json_req = json.loads(request.body)
        type_id = json_req['type_id']
        user_id = get_userid(json_req['token'])
        login_user = User.objects.get(user_id=user_id)
        # 先查询是否已经存在articleID
        article = Article.objects.filter(user_id=login_user, flag=3, title="")
        # article 已经存在则直接返回
        if article.exists():
            result = {'code': 200, 'article_id': article[0].article_id}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            article = Article(user_id=login_user, type_id=type_id, flag=3)
            # 保存文章
            article.save()
            result = {'code': 200, 'article_id': article.article_id}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")
