<template>
    <div>
        <div class="comment-title">
            <span class="maintitle">评论</span>
            <span class="all_comment">共有{{ comment_count }}条评论</span>
        </div>

        <!-- 发表评论 -->
        <div class="my-comment" >
            <img :src="user.user_url">
            <textarea v-model="mycomment" maxlength="100" ></textarea>
            <div class="corr">
                <em class="arrline">◆</em>
                <span class="arrclr">◆</span>
            </div>
            <el-button class="comment-btn" type="primary" @click="comment" :disabled="isNull">评论</el-button>
        </div>

        <!-- 用户评论 -->
        <div class="user-comments">
            <div class="comment-title">
                <span class="all_comment">用户评论</span>
            </div>
            <div class="comment-item no_comment" v-if="comments.length == 0">该文章还没有用户评论，快来抢沙发~</div>
            <div v-else>
            <div class="comment-item" v-for="item in comments" :key="item">
                <img :src="item.user_url" >
                <div class="comment-content">
                    <span class="content-username">{{ item.user_name }}：</span>
                    <span>{{ item.comment_content }}</span>
                </div>
                <div class="comment-time">{{ item.create_time }}</div>

                <!-- 查看回复icon -->
                <i class="el-icon-s-comment" @click="reply(item.comment_id)" v-if="responseShow != item.comment_id">查看回复</i>
                <i class="el-icon-s-comment" @click="responseShow=0" v-else>收起回复</i>

                <!-- 对评论的回复 -->
                <i class="el-icon-chat-round" @click="myresponse='',myresponseShow = item.comment_id" v-if="myresponseShow != item.comment_id">回复</i>
                <i class="el-icon-chat-round" @click="myresponseShow=0" v-else>取消回复</i>
                <i class="el-icon-delete" @click="delcomment(item.comment_id)" v-if="item.from_user_id == user.user_id">删除</i>

                <div class="my_response" v-if="myresponseShow == item.comment_id">
                    <img :src="user.user_url">
                    <el-input  class="myresponse_input" type="textarea" placeholder="请输入内容" v-model="myresponse" maxlength="100" show-word-limit></el-input>
                    <el-button class="comment-btn" type="primary" @click="replyComment(item.comment_id, item.user_id)">发送</el-button>
                </div>

                <!-- 回复信息列表 -->
                <div class="response" v-if="responseShow == item.comment_id">
                    <div class="comment-item" v-if="response.length == 0">该评论下无回复~</div>
                    <div v-else>
                        <div class="comment-item" v-for="res in response" :key="res">
                            <img :src="res.from_user_url" >
                            <div class="comment-content">
                                <span class="content-username">{{ res.from_user_name }} <span class="huifu">回复</span> {{ res.to_user_name }}：</span>
                                <span>{{ res.reply_content }}</span>
                            </div>
                            <div class="comment-time">{{ res.create_time }}</div>
                            <i class="el-icon-chat-round" @click="myreplytoreply='',myreplyShow = res.reply_id" v-if="myreplyShow != res.reply_id">回复</i>
                            <i class="el-icon-chat-round" @click="myreplyShow=0" v-else>取消回复</i>
                            <i class="el-icon-delete" @click="delreply(res.reply_id)" v-if="res.from_user_id == user.user_id">删除</i>
                            <!-- 对回复的回复 -->
                            <div class="my_response" v-if="myreplyShow == res.reply_id">
                                <img :src="user.user_url">
                                <el-input  class="myresponse_input" type="textarea" placeholder="请输入内容" v-model="myreplytoreply" maxlength="100" show-word-limit></el-input>
                                <el-button class="comment-btn" type="primary" @click="replyreply(item.comment_id,res.reply_id, res.from_user_id)">发送</el-button>
                            </div>
                        </div>
                        <el-pagination small layout="prev, pager, next" page-size="10" :total="reply_count" @current-change="currentChange($event,item.comment_id)" > </el-pagination>
                    </div>
                </div>
            </div>
            <pagination :total="comment_count" @getNewList="getNewList"></pagination>
            </div>
            <!-- <el-pagination small layout="prev, pager, next" :total="50"></el-pagination> -->
        </div>
    </div>

</template>

<script>
    import articleApi from '../../api/article'
    import pagination from '../../components/pagination/pagination'
    import commentApi from '../../api/comment'
    import {getLocalStorage} from "../../utils/auth";

    export default {
        name: "comment",
        data(){
            return {
                responseShow: 0,
                myresponseShow: 0,
                myreplyShow: 0,
                isNull: true,
                mycomment:'', // 评论
                myresponse:'', // 对评论的回复
                myreplytoreply:'', // 对回复的回复
                user: {
                    token: getLocalStorage('token'),
                    user_id: getLocalStorage('user_id'),
                    user_name: getLocalStorage('user_name'),
                    user_url: getLocalStorage('user_url'),
                },
                comments: [],
                comment_count: 0,
                reply_count: 0,
                response: [],
                page: 1
            }
        },
        props:['article_id'],
        methods: {
            getNewList(val){ //评论的分页
                this.page = val;
                articleApi.getCommentInfo({
                    article_id: this.$route.query.id || this.article_id,
                    token:this.user.token,
                    page: this.page
                }).then(res => {
                    this.comments = res.comment;
                    this.comment_count = res.comment_count;
                })
            },
            currentChange(val,id) { // 回复的分页
                commentApi.getReplyInfo({
                    comment_id: id,
                    token:this.user.token,
                    page: val
                }).then(res => {
                    // console.log(res);
                    this.response = res.reply;
                    this.reply_count = res.reply_count;
                })
            },
            comment() { // 发表评论
                commentApi.addComment({
                    article_id: this.$route.query.id || this.article_id,
                    token:this.user.token,
                    comment_content: this.mycomment,
                    user_id: this.user.user_id
                }).then(res => {
                    this.comments.unshift(res.comment[0]);
                    this.comment_count++;
                    // console.log(res);
                    this.mycomment = '';
                    this.comment_count++
                })
            },
            reply(id) { // 获取回复列表信息
                commentApi.getReplyInfo({
                    comment_id: id,
                    token:this.user.token,
                    page: 1
                }).then(res => {
                    console.log(res);
                    this.response = res.reply;
                    this.reply_count = res.reply_count;
                    this.responseShow = id;
                })
            },
            replyComment(comment_id,user_id) { // 对评论的回复
                commentApi.addReplyToComment({
                    comment_id: comment_id,
                    token:this.user.token,
                    reply_content: this.myresponse,
                    from_user_id: user_id,
                    user_id: this.user.user_id
                }).then(res => {
                    console.log(res);
                    this.response.unshift(res.reply_comment[0]);
                    //this.comment_count++;
                    this.myresponse = '';
                    this.reply_count++;
                })
            },
            replyreply(comment_id,reply_id,user_id) { // 对回复的回复
                commentApi.addReplyToReply({
                    comment_id: comment_id,
                    reply_id: reply_id,
                    token:this.user.token,
                    user_id: this.user.user_id,
                    reply_content: this.myreplytoreply,
                    from_user_id: user_id
                }).then(res => {
                    console.log(res);
                    this.response.unshift(res.reply_reply[0]);
                    this.myreplytoreply = '';
                    this.reply_count++;
                })
            },
            delcomment(id) {
                commentApi.deleteComment({  // 删除评论
                    comment_id: id,
                    token:this.user.token
                }).then(() => {
                    let item = this.comments.find(item => item.comment_id == id);
                    this.comments.splice(this.comments.indexOf(item), 1);
                    this.comment_count--;
                })
            },
            delreply(id) {
                commentApi.deleteReply({  // 删除回复
                    reply_id: id,
                    token:this.user.token
                }).then(() => {
                    let item = this.response.find(item => item.reply_id == id);
                    this.response.splice(this.response.indexOf(item), 1);
                    this.reply_count--;
                })
            }
        },
        watch: {
            mycomment() {
                if(this.mycomment == '') this.isNull = true;
                return this.isNull = false;
            }
        },
        created(){
            articleApi.getCommentInfo({  // 获取评论列表
                article_id: this.$route.query.id || this.article_id,
                token:this.user.token,
                page:1
            }).then(res => {
                //console.log(res);
                this.comments = res.comment;
                this.comment_count = res.comment_count;
            })
        },
        components: {
            pagination
        }
    }
</script>

<style lang="scss" scoped>
    .comment-title {
        padding-bottom: 10px;
        border-bottom: 2px solid #8DAFFC;
        color: #333;
        font-size: 12px;
        .all_comment{
            color: #8590a6;
            font-size: 13px;
        }
    }
    .maintitle {
        color: black;
        font-size: 20px;
        display: inline-block;
        margin-right: 5px;
    }
    .my-comment {
        position: relative;
        margin:20px 0px;
        img {
            float: left;
            width: 60px;
            height: 60px;
            border: 1px solid #99999940;
            border-radius: 2px;
        }
        textarea {
            height: 75px;
            width: 84.2%;
            display: block;
            margin-left: 90px;
            padding: 5px 6px 6px;
            border: 1px solid #cdcdcd;
            border-radius: 2px;
            line-height: 19px;
            resize: none;
            overflow: auto;
            outline: none;
        }
        .corr {
            position: absolute;
            left: 82px;
            top: 23px;
            width: 13px;
            height: 14px;
            overflow: hidden;
        }
        .arrline {
            color: #cdcdcd;
            display: block;
            font-family: "SimSun";
            font-size: 15px;
            font-style: normal;
            font-weight: normal;
            height: 10px;
            line-height: normal;
            text-align: left;
        }
        .arrclr {
            margin: -10px 0 0 1px;
            color: #fff;
            display: block;
            font-family: "SimSun";
            font-size: 15px;
            font-style: normal;
            font-weight: normal;
            height: 10px;
            line-height: normal;
        }
        .comment-btn {
            float: right;
            right: 0px;
            margin-top: 10px;
        }
    }
    .user-comments {
        margin: 40px 0px 20px 0px;
        .comment-title {
            border-bottom: 1px solid #cfcfcf;
            padding-bottom: 5px;
            font-weight: bold;
        }
        .comment-item {
            margin-top: 20px;
            border-bottom: 1px solid #f6f6f6;
            padding-bottom: 10px;
            position: relative;
            img {
                float: left;
                width: 24px;
                height: 24px;
                border: 1px solid #99999940;
                border-radius: 2px;
            }
            i {
                font-size: 13px;
                color: #8590a6;
                margin-left: 31px;
                cursor: pointer;
            }
            i:hover {
                color: #76839b;
            }
            .comment-time {
                color: #999;
                position: absolute;
                right: 0px;
            }
        }
        .no_comment{
            text-align: center;
            font-size: 15px;
            color: #8590a6;
        }
        .comment-content {
            position: relative;
            font-size: 14px;
            width: 633px;
            display: block;
            margin-left: 25px;
            padding: 5px 6px 6px;
            .huifu {
                color: #000000;
            }
        }
        .content-username {
            color: #8DAFFC;
            text-decoration: none;
        }
        .pagination {
            margin: 10px -10px 0px 0px;
            float: right;
        }
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
    .response {
        margin: 0px 0px 24px 31px;
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
            width: 93%;
        }
        .el-pagination {
            margin: 10px -10px 0px 0px;
            float: right;
        }
    }

</style>
