import request from '@/utils/request'

export default {
    // 发表评论
    addComment(data){
        return request({
            url:'/comment/addComment',
            method:'post',
            data
        })
    },
    // 获取回复列表
    getReplyInfo(data) {
        return request({
            url:'/reply/queryReply',
            method:'post',
            data
        })
    },
    // 对评论的回复
    addReplyToComment(data) {
        return request({
            url:'/reply/addReplyToComment',
            method:'post',
            data
        })
    },
    // 对回复的回复
    addReplyToReply(data) {
        return request({
            url:'/reply/addReplyToReply',
            method:'post',
            data
        })
    },
    // 删除评论
    deleteComment(data) {
        return request({
            url:'/comment/deleteComment',
            method:'post',
            data
        })
    },
    // 删除回复
    deleteReply(data) {
        return request({
            url:'/reply/deleteReply ',
            method:'post',
            data
        })
    },
}