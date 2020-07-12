<template>
    <div>
        <div class="article_box" v-for="(item,index) in articles" :key="index">
            <div class="article_title">
                {{ item.title }}
                <el-tag>{{item.type_name}}</el-tag>
                <span class="article_time">{{ item.create_time }}</span>
                <el-button class="del_btn" icon="el-icon-minus" @click="del(item.article_id,index)" plain v-if="curuser_id === user.id"></el-button>
            </div>
            <div class="img_box" v-if="item.photo.photo_url">
                <img class="article_img" :src="item.photo.photo_url">
            </div>
            <div class="article_content">
                <span>{{ item.simple_content | articleFilter }}</span>
            </div>
            <div class="article_footer">
                <i class="el-icon-chat-line-square article_icon">{{ item.comment_count }}条评论</i>
                <i class="el-icon-view article_icon">浏览量{{ item.page_view }}</i>
                <i class="el-icon-thumb article_icon">点赞{{ item.point_count }}</i>
                <el-button type="primary" icon="el-icon-zoom-in" @click="detail(item.article_id)">查看全文</el-button>
            </div>
        </div>
        <pagination :total="article_count" @getNewList="getNewList" v-if="article_count"></pagination>
    </div>
</template>

<script>    // import api from '../../api/user'

    import articleApi from '../../api/article'
    import {getLocalStorage} from "../../utils/auth";
    import pagination from '../../components/pagination/pagination'

    export default {
        name: "myarticle",
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
                articleApi.delArticle({
                    token:getLocalStorage('token'),
                    article_id:id
                }).then(() => {
                    // console.log(res)
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
            getNewList(val) {
                articleApi.getLauchedArticleInfo({
                    token: this.user.token,
                    page: val,
                    user_id: this.curuser_id,
                }).then(res => {
                    // console.log(res);
                    this.articles = res.article;
                })
            }
        },
        created(){
            console.log(this.curuser_id)
            articleApi.getLauchedArticleInfo({
                token: this.user.token,
                page: 1,
                user_id: this.curuser_id,
            }).then(res => {
                // console.log(res);
                this.articles = res.article;
                this.article_count = res.article_count;
            })
        },
        components: {
            pagination
        }
    }
</script>

<style lang="scss" scoped>
    .article_box {
        height: 185px;
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
