<template>
    <div>
        <div v-for="(item,index) in articles" :key="index" class="eachcomment"> 
            <div class="mycomment">{{ item.comment_content }}
                <span class="article_time">{{ item.comment_create_time }}</span>
            </div>
            <div class="article_box">
                <div class="article_title">
                    {{ item.article.title }}
                </div>
                <div class="article_info">
                    <el-tag>{{item.article.type_name}}</el-tag>
                    <span class="info_item">作者：{{ item.article.user.user_name }}</span>
                    <span class="info_item">发布时间：{{ item.article.create_time }}</span>
                </div>
                <div class="img_box" v-if="item.photo.photo_url">
                    <img class="article_img" :src="item.photo.photo_url">
                </div>
                <div class="article_content">
                    <span>{{ item.article.simple_content | articleFilter }}</span>
                </div>
                <div class="article_footer">
                    <i class="el-icon-chat-line-square article_icon">{{ item.comment_count }}条评论</i>
                    <i class="el-icon-view article_icon">浏览量{{ item.article.page_view }}</i>
                    <i class="el-icon-thumb article_icon">点赞{{ item.article.point_count }}</i>
                    <el-button  class="article_btn" icon="el-icon-zoom-in" @click="detail(item.article.article_id)" plain>查看全文</el-button>
                </div>
            </div>
            <div class="comment_info" v-if="curuser_id === own.id">
                <el-button class="comment_btn" icon="el-icon-delete" @click="del(item.comment_id,index)" plain>删除评论</el-button>
                <el-button icon="el-icon-caret-bottom" @click="reply(item.comment_id)" v-if="!responseShow">查看回复</el-button>
                <el-button icon="el-icon-caret-top" @click="responseShow = 0" v-if="responseShow==item.comment_id">收起回复</el-button>
                <i class="el-icon-s-comment reply_count">共有{{ item.reply_count }}条回复</i>
            </div>
            
            <!-- 回复信息列表 -->
            <div class="response" v-if="responseShow == item.comment_id">
                <div class="comment-item" v-if="response.length == 0">该评论下无回复~</div>
                <div v-else>
                    <div class="comment-item" v-for="res in response" :key="res">
                        <img :src="res.to_user_url" >
                        <div class="comment-content">
                            <span class="content-username">{{ res.from_user_name }} <span class="huifu">回复</span> {{ res.to_user_name }}：</span>
                            <span>{{ res.reply_content }}</span>
                        </div>
                        <div class="comment-time">{{ res.create_time }}</div>
                        <i class="el-icon-chat-round" @click="myreplytoreply='',myreplyShow = res.reply_id" v-if="myreplyShow != res.reply_id">回复</i>
                        <i class="el-icon-chat-round" @click="myreplyShow=0" v-else>取消回复</i>
                        <i class="el-icon-delete" @click="delreply(res.reply_id)" v-if="res.from_user_id == own.id">删除</i>
                        <!-- 对回复的回复 -->
                        <div class="my_response" v-if="myreplyShow == res.reply_id">
                            <img :src="own.user_url">
                            <el-input  class="myresponse_input" type="textarea" placeholder="请输入内容" v-model="myreplytoreply" maxlength="100" show-word-limit></el-input>
                            <el-button class="comment-btn" type="primary" @click="replyreply(item.comment_id,res.reply_id, res.from_user_id)">发送</el-button>
                        </div>
                    </div>
                    <el-pagination small layout="prev, pager, next" page-size="10" :total="reply_count" @current-change="currentChange($event,item.comment_id)" > </el-pagination>
                </div>
            </div>

        </div>
        <pagination :total="article_count" @getNewList="getNewList" v-if="article_count"></pagination>
    </div>
</template>

<script>
    import api from '../../api/article'
    import commentApi from '../../api/comment'
    import {getLocalStorage} from "../../utils/auth";
    import pagination from '../../components/pagination/pagination'

    export default {
        name: "myarticle",
        data(){
            return {
                own: {
                    id: getLocalStorage('user_id'),
                    token: getLocalStorage('token'),
                    user_url: getLocalStorage('user_url')
                },
                articles: [],
                my_comment: '我的第一条评论',
                article_count: 0,
                responseShow: '',
                reply_count: 0,
                response:[],
                myreplyShow: '',
                myreplytoreply:'', // 对回复的回复
            }
        },
        props:['curuser_id'],
        methods: {
            del(id,index) {
                commentApi.deleteComment({
                    token: this.own.token,
                    comment_id:id
                }).then(res => {
                    console.log(res)
                    this.articles.splice(index, 1);
                    this.article_count--;
                })
            },
            detail(id) {
                let routeUrl = this.$router.resolve({
                    path:'/articleDetail',
                    query:{id:id}
                })
                window.open(routeUrl.href,"_blank")
            },
            getNewList(val) { // 文章分页
                api.getCommentArticleInfo({
                    user_id: this.curuser_id,
                    token: this.own.token,
                    page: val
                }).then(res => {
                    this.articles = res.data;
                })
            },
            reply(id) { // 回复列表
                commentApi.getReplyInfo({
                    comment_id: id,
                    token: this.own.token,
                    page: 1
                }).then(res => {
                    this.response = res.reply;
                    console.log(this.response);
                    this.reply_count = res.reply_count;
                    this.responseShow = id;
                })
            },
            delreply(id) {
                commentApi.deleteReply({  // 删除回复
                    reply_id: id,
                    token:this.own.token
                }).then(() => {
                    let item = this.response.find(item => item.reply_id == id);
                    this.response.splice(this.response.indexOf(item), 1);
                    this.reply_count--;
                })
            },
            replyreply(comment_id,reply_id,user_id) { // 对回复的回复
                commentApi.addReplyToReply({
                    comment_id: comment_id,
                    reply_id: reply_id,
                    token:this.own.token,
                    user_id: this.own.id,
                    reply_content: this.myreplytoreply,
                    from_user_id: user_id
                }).then(res => {
                    console.log(res);
                    this.response.unshift(res.reply_reply[0]);
                    this.myreplytoreply = '';
                    this.reply_count++;
                })
            },
            currentChange(val,id) { // 回复的分页
                commentApi.getReplyInfo({
                    comment_id: id,
                    token:this.own.token,
                    page: val
                }).then(res => {
                    this.response = res.reply;
                })
            },
        },
        created(){
            api.getCommentArticleInfo({
                user_id: this.curuser_id,
                token: this.own.token,
                page:1
            }).then(res => {
                // console.log(res);
                this.articles = res.data;
                this.article_count = res.article_count;
            })
        },
        filters:{
            articleFilter(content){
                return content + '...'
            }
        },
        components: {
            pagination
        }
    }
</script>

<style lang="scss" scoped>
    .eachcomment {
        border-bottom: 1px solid #f7f8fa;
        margin-bottom: 20px;
    }
    .mycomment {
        // font-weight: 600;
        font-size: 18px;
        margin-bottom: 10px;
        .del_btn {
            float: right;
        }
        .del_btn:hover {
            color: #fff;
        }
    }
    .el-button {
        margin-left: 10px;
        padding: 8px 10px;
    }
    .comment_info {
        font-weight: 400;
        font-size: 14px;
        color: #909399;
        margin: 10px 0px;
        .reply_count {
            margin-left: 5px; 
            vertical-align: bottom;
            font-size: 14px;
        }
        .comment_btn {
            margin-left: 0px;
            color: #8DAFFC;
            border-color: #8DAFFC;
        }
        .comment_btn:hover {
            color: #8DAFFC !important;
            border-color: #8DAFFC !important;
            background-color: #f4f7ff !important;
        }
    }
    .article_time {
        font-weight: 400;
        font-size: 14px;
        color: #909399;
        line-height: 24px;
        margin-left: 5px;
        float: right;
    }
    .article_box {
        height: 220px;
        padding: 20px 20px;
        position: relative;
        // border: 1px solid #f7f8fa;
        box-shadow: 0 0px 15px rgba(26, 26, 26, 0.1);
        border-radius: 5px;
        .article_title {
            height: 30px;
            font-weight: 600;
            font-size: 18px;
            margin: 0px 5px;
        }
        .article_info {
            margin-bottom: 10px;
        }
        .info_item {
            font-weight: 400;
            font-size: 14px;
            color: #909399;
            vertical-align: bottom;
            margin: 0px 5px;
        }
        .img_box {
            width: 180px;
            height: 120px;
            float: left;
            margin-right: 20px;
            border-radius: 5px;
            overflow: hidden;
            position: relative;
        }
        .article_img {
            position: absolute;
            top:-27%;
            left: -20%;
            width: 250px;
        }
        .article_content {
            height: 120px;
            vertical-align: top;
            font-size: 15px;
            line-height: 30px;
            span {
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 4;
                -webkit-box-orient: vertical;
            }
        }
        .article_footer {
            float: right;
        }
        .article_btn:hover {
            color: #8DAFFC !important;
            border-color: #8DAFFC !important;
            background-color: #fff !important;
        }
        .article_icon {
            font-size: 15px;
            color: #909399;
            vertical-align: middle;
            margin-left: 10px;
        }
    }
    .article_box::after {
        content: "";
        position: absolute;
        right: 20px;
        left: 20px;
        bottom: 0;
        height: 1px;
        background-color: #f7f8fa;
    }
    .response {
        box-shadow: 0 0px 15px rgba(26, 26, 26, 0.1);
        border-radius: 5px;
        padding: 0px 10px 40px 10px;
        .comment-item {
            border-bottom: 0;
            border-top: 1px solid #f6f6f6;
            margin-top: 10px;
            padding-top: 10px;
        }
        .comment-content {
            width: 602px;
        }
        .myresponse_input {
            width: 572px;
        }
        .el-pagination {
            margin: 10px -10px 0px 0px;
            float: right;
        }
        .my_response {
            margin: 10px 0px 0px 31px;
            border-top: 1px solid #f6f6f6;
            padding-top: 10px;
            height: 80px;
            .myresponse_input {
                display: inline-block;
                margin-left: 10px;
                width: 94%;
            }
            .comment-btn {
                float: right;
                padding: 5px 10px;
                font-size: 12px;
                margin-top: 10px;
            }
            i {
                float: right;
                margin-top: 16px;
                margin-right: 10px;
            }
        }
        img {
            float: left;
            width: 24px;
            height: 24px;
            border: 1px solid #99999940;
            border-radius: 2px;
            margin-right: 5px;
        }
        i {
            margin-right: 31px;
            font-size: 13px;
            color: #8590a6;
            margin-top: 3px;
            cursor: pointer;
        }
        i:hover {
            color: #76839b;
        }
        .comment-time {
            color: #999;
            position: absolute;
            right: 30px;
        }
        .content-username {
            color: #8DAFFC;
            text-decoration: none;
        }
        .huifu {
            color: #000000;
        }
    }
</style>
