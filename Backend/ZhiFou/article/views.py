
from django.db import connection
from Tool.decorator import check_request, execute_sql
from article.dao import ArticleDao



# 获取首页文章的缩略图 falg=0 图片，falg=3 视频的截图
# article_id  文章ID号
def getArticlePhoto(article_id):
    sql = ArticleDao.getArticlePhoto()
    args = (article_id,)
    photo = execute_sql(sql, args)
    return photo


# 获取用户已收藏文章数量
# user_id     用户id
def getCollectionArticleCount(user_id):
    sql = ArticleDao.getCollectionArticleCount()
    args = (user_id,)
    cur = connection.cursor()
    article_count = cur.execute(sql, *args)
    cur.close
    return article_count

# 查询用户是否对该文章点赞
def queryPoint(user_id, article_id):
    sql = ArticleDao.queryPoint()
    args = (user_id, article_id)
    cur = connection.cursor()
    pointFlag = cur.execute(sql, args)
    cur.close
    return pointFlag

