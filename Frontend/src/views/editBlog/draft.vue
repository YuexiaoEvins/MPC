<template>
    <div>
        <Nav style="position:sticky;"></Nav>
        <div class="main">
            <div class="title">草 稿 箱</div>
            <div v-if="articles.length">
                <div class="article_box" v-for="(item,index) in articles" :key="index">
                    <div class="article_title">
                        {{ item.title }}
                        <el-tag>{{item.type_name}}</el-tag>
                        <span class="article_time">{{ item.create_time }}</span>
                    </div>
                    <img class="article_img" :src="item.photo_url" v-if="item.photo_url">
                    <div class="article_content">
                        <span>{{ item.simple_content }}</span>
                    </div>
                    <div class="btn">
                        <el-button type="primary" icon="el-icon-edit-outline" @click="editArticle(item.article_id)">编辑</el-button>
                        <el-button type="danger" icon="el-icon-delete" @click="delArticle(item.article_id,index)">删除</el-button>
                    </div>
                </div>
                <pagination :total="total" @getNewList="getNewList"></pagination>
            </div>
            <div class="nulldraft" v-else>
                很干净！赶紧去发布文章吧！
                <el-button class="edit_btn" @click="$router.push('/editBlog')" plain>去发布</el-button>
            </div>
        </div>
    </div>
</template>

<script>
    import Nav from '../../components/navBar/nav'
    import api from '../../api/article'
    import pagination from '../../components/pagination/pagination'
    import articleDetail from "../articleDetail/articleDetail";
    import {getLocalStorage} from "../../utils/auth";

    export default {
        name: "userinfo",
        data(){
            return {
                sex: 1,
                activeName: 'myarticle',
                page:1,
                user:{
                },
                articles: [],
                total:''
            }
        },
        components: {
            Nav,
            pagination
        },
        methods: {
            goEditInfo() {
                this.$router.push('/editinfo')
            },
            delArticle(id,index){
                api.delArticle({token:getLocalStorage('token'),article_id:id}).then(res => {console.log(res),this.articles.splice(index,1)})
            },
            getNewList(val){
                this.page = val;
                this.getDraft()
            },
            getDraft(){
                api.getDraftArticle({token:getLocalStorage('token'),page:this.page,user_id:getLocalStorage('user_id')}).then(res =>
                {
                    console.log(res)
                this.total = res.article_count
                this.articles = res.article;
                })
            },
            editArticle(articleId){
                this.$router.push({
                    path:'/editBlog',
                    query:{articleId:articleId,ifEdit:true}
                })
            }
        },
        created(){
           this.getDraft()
            },
    }
</script>

<style lang="scss" scoped>
    .main{
        width: 940px;
        margin: 10px auto;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
        padding: 50px 30px;
    }
    .title {
        color: #8DAFFC;
        font-size: 25px;
        font-weight: 600;
        padding-bottom: 10px;
        border-bottom: 2px solid #8DAFFC;;
    }
    .article_box {
        padding: 20px;
        padding-bottom: 50px;
        position: relative;
        overflow: hidden;
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
            float: right;
        }
        .el-tag {
            font-weight: 400;
        }
        .del_btn {
            float: right;
        }
        .article_img {
            width: 200px;
            border-radius: 5px;
            float: left;
            margin-right: 20px;
        }
        .article_content {
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
        .btn {
            float: right;
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
    .nulldraft {
        margin-top: 20px;
        font-size: 14px;
        color: #999;
        .edit_btn {
            font-size: 12px;
            padding: 5px;
            color: #8DAFFC;
            border-color: #8DAFFC;
        }
        .edit_btn:hover {
            color: #8DAFFC !important;
            border-color: #8DAFFC !important;
            background-color: #f4f7ff !important;
        }
    }
</style>
