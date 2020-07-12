from Tool.page_tool import PageInfo
from article.models import Reply


#删除回复
def del_reply_info(reply_id):
    try:
        r=Reply.objects.filter(reply_id=reply_id).update(is_delete=0)
        return r
    except:
        print("删除回复失败")


#分页查询回复
def query_reply_info(comment_id,page):
    try:
        page_info = PageInfo(page,10)
        replyList = Reply.objects.filter(comment_id=comment_id,is_delete=1).order_by('-create_time')[page_info.start():page_info.end()]
        return replyList
    except:
        print("分页查询回复失败")



#查看评论下的回复数量：
def query_reply_count(comment_id):
    try:
        reply_count = Reply.objects.filter(comment_id=comment_id, is_delete=1).count()
        return reply_count
    except:
        print("fail")