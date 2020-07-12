from django.urls import path

from article.service import DraftBox, UploadPhoto, UploadArticle, searchArticle, CollectAndPoint, PersonalPage, \
    HomePage, MessageBoard
from article.service.searchArticle import MySearchView

urlpatterns = [
    path('search', MySearchView(), name='haystack_search'),  #搜索文章
    path('delHistorySearch', searchArticle.delHistorySearch),  # 删除历史记录
    path('delAllHistorySearch', searchArticle.delAllHistorySearch),  # 删除全部历史记录
    path('rankSearch', searchArticle.rankSearch),  # 热词返回

    # 首页
    path('queryArticle', HomePage.queryArticle),  # 首页查询
    path('readFullArticle', HomePage.readFullArticle),  # 阅读全文
    path('queryArticleByTypeId', HomePage.queryArticleByTypeId),  # 分类查询
    path('queryArticleDetailed', HomePage.queryArticleDetailed),  # 查看文章详情
    path('getIndexPhoto', HomePage.getIndexPhoto),  # 获取首页的轮播图片地址

    # 个人主页
    path('queryArticleByMyself', PersonalPage.queryArticleByMyself),  # 用户已发帖子
    path('queryCollectionByUserId', PersonalPage.queryCollectionByUserId),  # 用户已收藏文章
    path('queryCommentByUserId', PersonalPage.queryCommentByUserId),  # 查询用户已评论文章
    path('queryPointByUserId', PersonalPage.queryPointByUserId),  # 查询用户已点赞文章

    # 收藏及点赞
    path('collecteArticle', CollectAndPoint.collecteArticle),  # 收藏功能
    path('pointArticle', CollectAndPoint.pointArticle),  # 点赞功能

    # 上传图片或者视频
    path('uploadPhoto', UploadPhoto.uploadPhoto),

    # 上传文章删除文章
    path('createArticleId', UploadArticle.createArticleId),  # 生成文章ID
    path('delArticleOrDraft', UploadArticle.delArticleOrDraft),  # 删除文章或者草稿
    path('saveArticle', UploadArticle.saveArticle),  # 保存文章（发表文章或者保存草稿）

    # 草稿箱
    path('queryDraftBox', DraftBox.queryDraftBox),  # 查看草稿箱信息
    path('editorDraftBox', DraftBox.editorDraftBox),  # 编辑草稿箱信息

    # 留言板
    path('queryMessageBoard', MessageBoard.queryMessageBoard),  # 查询留言信息
    path('addMessageBoard', MessageBoard.addMessageBoard),  # 新增留言板信息
    path('deleteMessageBoard', MessageBoard.deleteMessageBoard),  # 删除留言信息
    path('queryMessageBoardByUserId', MessageBoard.queryMessageBoardByUserId),  # 查询用户的已发留言信息
]
