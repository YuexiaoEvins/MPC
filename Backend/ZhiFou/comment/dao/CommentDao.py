import json

from django.http import HttpResponse

from article.models import Comment, Reply


# 获取文章评论数量
# article_id  文章ID号
def getArticleCommentCount(article_id):
    try:
        count = Comment.objects.filter(article_id=article_id, is_delete=1).count()
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}), content_type="application/json")
    return count


#批量获取文章评论数量的接口
def query_comment_count(articles):
    json_list=[]
    try:
        for i in articles:
            comment = Comment.objects.filter(article_id=i).count()
            dic={"comment_count":comment}
            json_list.append(dic)
        return json_list
    except:
        print("获取评论数量失败")
        return json_list

#删除评论
def del_comment_info(comment_id):
    try:
        r=Comment.objects.filter(comment_id=comment_id).update(is_delete=0)
        return r
    except:
        print("删除评论失败")