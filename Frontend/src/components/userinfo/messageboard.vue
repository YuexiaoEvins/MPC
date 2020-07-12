<template>
    <div>
        <div class="article_box" v-for="(item,index) in articles" :key="index">
            <div class="article_content">
                <el-button class="del_btn" icon="el-icon-minus" @click="del(item.board_id,index)" plain v-if="curuser_id === user.id"></el-button>
<!--                <span>{{ item.content }}</span>-->
                <span v-html="item.content"></span>
            </div>
            <div class="article_footer">
                <span class="article_time">{{ item.create_time }}</span>
            </div>
        </div>
        <pagination :total="article_count" @getNewList="getNewList" v-if="article_count"></pagination>
    </div>
</template>

<script>
    import articleApi from '../../api/article'
    import {getLocalStorage} from "../../utils/auth";
    import pagination from '../../components/pagination/pagination'

    export default {
        name: "messageboard",
        data(){
            return {
                user:{
                    id: getLocalStorage('user_id'),
                    token: getLocalStorage('token')
                },
                articles: [],
                article_count: 0,
            }
        },
        props:['curuser_id'],
        filters:{
            articleFilter(content){
                return content + '...'
            }
        },
        methods: {
            del(id,index) {
                articleApi.deleteMessageBoard({
                    token:getLocalStorage('token'),
                    board_id:id
                }).then(res => {
                    console.log(res)
                    this.articles.splice(index, 1);
                    this.article_count--;
                })
            },
            getNewList(val) {
                articleApi.getLauchedArticleInfo({
                    token: this.user.token,
                    page: val,
                    user_id: this.curuser_id,
                }).then(res => {
                    console.log(res);
                    this.articles = res.article;
                })
            }
        },
        created(){
            console.log(this.curuser_id)
            articleApi.getUserMessageBoardInfo({
                token: this.user.token,
                page: 1,
                user_id: this.curuser_id,
            }).then(res => {
                console.log(res);
                this.articles = res.board;
                this.article_count = res.board_count;
            })
        },
        components: {
            pagination
        }
    }
</script>

<style lang="scss" >
    @import "../../assets/css/emoji.css"; // 导入精灵图样式
    .comment-wrap {
        width: 680px;
        margin-bottom: 30px;
        .emoji-item-common {
            background: url("../../assets/img/emoji_sprite.png");
            display: inline-block;
            &:hover {
                cursor: pointer;
            }
        }
        .emoji-size-small {
            // 表情大小
            zoom: 0.3;
        }
        .emoji-size-large {
            zoom: 0.5; // emojipanel表情大小
            margin: 4px;
        }
    }
    .article_box {
        height: 140px;
        padding: 20px 20px;
        position: relative;
        margin-bottom: 10px;
        .article_title {
            height: 30px;
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .article_time {
            font-weight: 400;
            font-size: 14px;
            color: #909399;
            vertical-align: bottom;
            margin-left: 5px;
        }
        .del_btn {
            float: right;
        }
        .del_btn:hover {
            color: #fff;
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
        .article_icon {
            font-size: 15px;
            color: #909399;
            vertical-align: middle;
            margin-left: 10px;
        }
        .el-button {
            margin-left: 10px;
            padding: 10px 10px;
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
</style>
