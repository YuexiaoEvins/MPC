import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from Tool.decorator import check_request
from article.dao.ArticleDao import query_page_view, getTypeName, queryPoint, queryUserInfo, queryPhotoInfo
from comment.dao.CommentDao import getArticleCommentCount
from users.utils.token_op import get_userid


class MySearchView(SearchView):
    def create_response(self):
        context = super().get_context()                   #搜索引擎完成后的内容
        keyword = self.request.GET.get('q', None)        # 关键词为q
        try:
            if not keyword:
                return HttpResponse(json.dumps({'code': 200, 'message': '没有相关信息'}), content_type="application/json")
            else:
                conn = get_redis_connection('default')
                article_count = SearchQuerySet().using("default").filter(text=keyword).count()  # 获取文章数量
                if article_count != 0:
                    conn.expire('keyword', 720 * 60)
                    conn.zincrby('keyword', 1, keyword)  # 搜索词存进redis
                #我搜索的历史记录的保存
                user_id =self.request.GET.get('q_uid',None)
                ##如果user_id不为空
                if user_id:
                    history_key = "history_%d" % int(user_id)
                    # 移除相同的记录
                    conn.lrem(history_key, 0, keyword)
                    # 从左侧添加历史浏览记录
                    conn.lpush(history_key, keyword)
                    # 只保留最新的五个历史浏览记录
                    conn.ltrim(history_key, 0, 4)
                #获取搜索文章信息
                content_list = []
                for i in context['page'].object_list:             #对象列表
                    set_dict = {
                        "article_id": i.object.article_id,
                        "title": i.object.title,
                        "simple_content": i.object.simple_content,
                        "page_view": query_page_view(i.object.article_id),
                        "create_time":  i.object.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "type_id": i.object.type_id,
                        "type_name": getTypeName(i.object.type_id),
                        "point_count": i.object.point_count,
                        "point_flag": queryPoint(user_id, i.object.article_id),
                        "user": queryUserInfo(i.object.user_id.user_id),
                        "photo": queryPhotoInfo(i.object.article_id),
                        "comment_count": getArticleCommentCount(i.object.article_id),
                     }  # 要返回的字段
                    content_list.append(set_dict)
                result = {'code': 200,'article_count':article_count, 'article': content_list}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")


#热搜的关键词返回接口
def queryRankSearch():
    try:
        Conn = get_redis_connection('default')
        # 取前五的搜索热词的关键字
        search_ranking = Conn.zrange("keyword", 0, 4, desc=True, withscores=True,score_cast_func=int)
        json_list=[]
        for item in search_ranking:
            # 遍历列表，将列表中的value值输出来
                set_dict = { "keyword":item[0].decode("utf-8")}
                json_list.append(set_dict)
        return json_list
    except:
        print("热搜获取失败")
        return json_list

#历史记录返回接口
def queryHistorySearch(user_id):
    try:
        json_list = []
        con = get_redis_connection('default')
        history_key = 'history_%d' % user_id
        # 获取用户最新浏览的5个搜索历史
        sku_ids = con.lrange(history_key, 0, 4)
        for item in sku_ids:
            # 遍历列表，将列表中的value值输出来
            set_dict = { "word": item.decode("utf-8"),}
            json_list.append(set_dict)
        return json_list
    except:
        print("历史记录获取失败")
        return json_list



#清空一个历史记录
@csrf_exempt
@check_request('token', 'word')
#@checkToken ("")
def delHistorySearch(request):
    try:
        json_req = json.loads(request.body)
        word = json_req['word']
        user_id = get_userid(json_req['token'])
        history_key = "history_%d" % user_id
        conn = get_redis_connection('default')
        # 移除记录
        conn.lrem(history_key, 0, word)
        return HttpResponse(json.dumps({'code': 200}))
    except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False))


#清空全部历史记录
@csrf_exempt
@check_request('token')
#@checkToken ("")
def delAllHistorySearch(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])
        conn = get_redis_connection('default')
        history_key = "history_%d" % user_id
        # 移除全部记录
        conn.delete(history_key)
        return HttpResponse(json.dumps({'code': 200}))
    except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False))


#热搜榜单+历史记录返回
@csrf_exempt
@check_request('token')
#@checkToken ("")
def rankSearch(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])
        json_list=queryRankSearch()
        sku_ids=queryHistorySearch(user_id)
        result = {'code': 200, 'search': json_list,'history':sku_ids}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False))


#清空全部历史记录
@csrf_exempt
@check_request('token')
#@checkToken ("")
def delAllHistorySearch(request):
    try:
        json_req = json.loads(request.body)
        user_id = get_userid(json_req['token'])
        conn = get_redis_connection('default')
        history_key = "history_%d" % user_id
        # 移除全部记录
        conn.delete(history_key)
        return HttpResponse(json.dumps({'code': 200}))
    except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False))

