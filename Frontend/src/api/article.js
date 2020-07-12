import request from '@/utils/request'

export default {
    // 获取首页文章列表
    getIndexInfo(data){
        return request({
            url:'/article/queryArticle',
            method:'post',
            data
        })
    },
    // 获取文章详情页信息
    getDetailInfo(data) {
        return request({
            url:'/article/queryArticleDetailed',
            method:'post',
            data
        })
    },
    // 获取文章所有评论信息
    getCommentInfo(data) {
        return request({
            url:'/comment/queryComment',
            method:'post',
            data
        })
    },
    // 阅读文章全文
    getFullArticle(data){
        return request({
            url:'/article/readFullArticle',
            method:'post',
            data
        })
    },
    //根据分类查询文章接口
    getQueryArticle(data){
        return request({
            url:'/article/queryArticleByTypeId',
            method:'post',
            data
        })
    },
    //进入页面生成文章ID
    createArticleId(data){
        return request({
            url:'/article/createArticleId',
            method:'post',
            data
        })
    },
    // 上传文章和视频
    uploadPhoto(data){
        return request({
            url:'/article/uploadPhoto',
            headers: {
            'Content-Type': 'multipart/form-data' //设置post文件的请求头
            },
            method:'post',
            data
        })
    },
    //发布文章或者保存到草稿
    saveArticle(data){
        return request({
            url:'/article/saveArticle',
            method:'post',
            data
        })
    },
    //获取草稿箱文章
    getDraftArticle(data){
        return request({
            url:'/article/queryDraftBox',
            method:'post',
            data
        })
    },
    //删除文章接口
    delArticle(data){
        return request({
            url:'/article/delArticleOrDraft',
            method:'post',
            data
        })
    },
    //编辑文章接口
    editArticle(data){
        return request({
            url:'/article/editorDraftBox',
            method:'post',
            data
        })
    },
    //搜索文章接口
    searchArticle(q,page,id){
        return request({
            url:'/article/search',
            method:'get',
            params:{q:q,page:page,q_uid:id}
        })
    },
    //返回热词搜索接口
    popularSearch(data){
        return request({
            url:'/article/rankSearch',
            method:'post',
            data
        })
    },
    //点赞文章接口
    addLikes(data){
        return request({
            url:'/article/pointArticle',
            method:'post',
            data
        })
    },
    //收藏文章接口
    addCollect(data){
        return request({
            url:'/article/collecteArticle',
            method:'post',
            data
        })
    },
    // 获取用户已发文章列表
    getLauchedArticleInfo (data) {
        return request({
        url: '/article/queryArticleByMyself',
        method: 'post',
        data
        })
    },
    // 获取用户收藏的文章列表
    getCollectionArticleInfo (data) {
        return request({
        url: '/article/queryCollectionByUserId',
        method: 'post',
        data
        })
    },
    // 获取用户点赞的文章列表
    getPointArticleInfo (data) {
        return request({
        url: '/article/queryPointByUserId',
        method: 'post',
        data
        })
    },
    // 获取用户评论的文章列表
    getCommentArticleInfo (data) {
        return request({
        url: '/article/queryCommentByUserId',
        method: 'post',
        data
        })
    },

    getIndexAd() {
        return request({
            url: "/article/getIndexPhoto",
            method: 'get'
        })
    },
    // 获取留言板
    getMessageBoardInfo(data) {
        return request({
            url: '/article/queryMessageBoard',
            method: 'post',
            data
        })
    },
    // 发布留言
    addMessageBoard(data) {
        return request({
            url: '/article/addMessageBoard',
            method: 'post',
            data
        })
    },
    // 查看个人留言
    getUserMessageBoardInfo(data) {
        return request({
            url: '/article/queryMessageBoardByUserId',
            method: 'post',
            data
        })
    },
    // 删除个人留言
    deleteMessageBoard(data) {
        return request({
            url: '/article/deleteMessageBoard',
            method: 'post',
            data

        })
    }
}
