import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Tool.decorator import check_request
from Tool.page_tool import PageInfo
from article.models import User, Comment
from comment.dao.CommentDao import del_comment_info
from users.utils.user_info import query_users_info
from users.views import add_address_profile_url
from users.utils.token_op import checkToken

#发表评论
#comment_content  评论的内容
#article_id       文章ID
#user_id          登录用户
@csrf_exempt
@check_request('comment_content', 'article_id','user_id')
@checkToken ("")
def addComment(request):
    json_req = json.loads(request.body)
    comment_content = json_req['comment_content']
    article_id = json_req['article_id']
    user_id = json_req['user_id']
    try:
        login_user = User.objects.get(user_id=user_id)
        # 插入评论信息
        comment = Comment.objects.create(comment_content=comment_content, article_id=article_id,user_id=login_user)
        print(comment)
        json_list = []
        json_dict = { "comment_id": comment.comment_id,
                      "comment_content": comment.comment_content,
                      "create_time": comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                      "user_id": login_user.user_id,
                      "user_name": login_user.user_name,
                      "user_url": add_address_profile_url(login_user.user_url),
                    }
        json_list.append(json_dict)
        result = {'code': 200, 'comment': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")


# 删除评论
# comment_id  评论ID
#  根据评论的ID进行软删除，把标志位改为0
@csrf_exempt
@check_request('comment_id')
@checkToken ("")
def deleteComment(request):
    json_req = json.loads(request.body)
    comment_id = json_req['comment_id']
    try:
        r = del_comment_info(comment_id=comment_id)
        if r == 1:
            return HttpResponse(json.dumps({'code': 200}))
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")



# 查看评论
# article_id  文章ID号
# user_id     用户ID
# page        页码
# 根据文章ID查询该文章的所有评论，返回评论信息和登录用户信息
@csrf_exempt
@check_request('article_id','page')
@checkToken ("")
def queryComment(request):
    json_req = json.loads(request.body)
    article_id = json_req['article_id']
    page = json_req['page']
    try:
        # 分页查询评论信息
        page_info = PageInfo(page, 10)
        comment_count = Comment.objects.filter(article_id=article_id, is_delete=1).count()  # 有效评论的总数量
        commentList = Comment.objects.filter(article_id=article_id, is_delete=1).order_by('-comment_id')[page_info.start():page_info.end()]
        # 单独返回user_id，进行批量查询用户信息操作 （values_list：返回一个可迭代的元祖序列）
        user_ids = list(commentList.values_list("user_id", flat=True))
        user = query_users_info(user_ids)
        i=0
        json_list = []
        for comment in commentList:
            json_dict = {"comment_id": comment.comment_id,
                         "comment_content": comment.comment_content,
                         "create_time": comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "user_id":user[i]['user_id'],
                         "user_name":user[i]['user_name'],
                         "user_url":user[i]['user_url']
                         }
            i=i+1
            json_list.append(json_dict)
        result = {'code': 200, 'comment_count': comment_count, 'comment': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False), content_type="application/json")