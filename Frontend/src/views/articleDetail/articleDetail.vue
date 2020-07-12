
<template>
<div>
    <Nav style="position:sticky;"></Nav>
    <div class="main">
        <!-- 标题 -->
        <div class="title_main">
            <div class="title">{{ article.title }}</div>
            <div class="tags"><el-tag>{{article.type_name}}</el-tag></div>
            <!-- 收藏功能未完成 -->
            <el-button type="primary" icon="el-icon-star-on" @click="store">{{ store_name }}</el-button>
            <el-button type="primary" icon="el-icon-edit" @click="jump">写评论</el-button>
            <i class="el-icon-chat-line-square article_icon">{{ article.comment_count }}条评论</i>
            <div class="hot_info">
                <div class="star_account">
                    <div class="hot_title">被收藏</div>
                    <strong>{{ article.collection_count }}</strong>
                </div>
                <div class="comment_account">
                    <div class="hot_title">被浏览</div>
                    <strong>{{ article.page_view }}</strong>
                </div>
            </div>
        </div>

        <!-- 正文 -->
        <div class="article_main">
            <div class="article_content" v-html="article.content"></div>
            <!-- {{ article.content }} -->
            <div class="article_time">{{ article.create_time }}</div>
            <i class="el-icon-chat-line-square article_icon">{{ article.comment_count }}条评论</i>
             <!-- 收藏点赞功能未完成 -->
            <el-button type="primary" icon="el-icon-star-on" @click="store">{{ store_name }}</el-button>
            <el-button type="primary" class="like_btn" icon="el-icon-thumb" @click="point">{{ point_name }} {{article.point_count}}</el-button>
        </div>

        <!-- 作者 -->
        <div class="user_main">
            <div class="user_title">关于作者</div>
            <div class="user_info">
                <img :src="article.user.user_url" class="user_avatar" @click="userinfo(article.user.user_id)">
                <div class="user_name" @click="userinfo(article.user.user_id)">{{ article.user.user_name }}</div>
                <i class="el-icon-medal level_name">{{ article.level_name }}</i>
                <div class="user_like">
                    <div class="article">
                        <div class="hot_title">文章</div>
                        <strong>{{ article.write_count }}</strong>
                    </div>
                    <div class="collection">
                        <div class="hot_title">获赞</div>
                        <strong>{{ article.user_point_count }}</strong>
                    </div>
                    <div class="credit">
                        <div class="hot_title">积分</div>
                        <strong>{{ article.user.user_credit }}</strong>
                    </div>
                </div>
                <el-button type="primary" class="chat_btn" icon="el-icon-chat-dot-round" @click="chat(article.user.user_id)">私信</el-button>
            </div>
        </div>
        <!-- 评论 -->
        <div class="comment_main" id="comment">
            <comment></comment>
        </div>
    </div>
</div>
</template>

<script>
    import Nav from '../../components/navBar/nav'
    import comment from '../../components/comment/comment'
    import articleApi from '../../api/article'
    import {getLocalStorage} from "../../utils/auth";

    export default {
        name: "articleDetail",
        data(){
            return {
                user: {},
                article: {},
                store_name: '',
                point_name: ''
            }
        },
        methods: {
            jump() { // 跳转到写评论
                let ele = document.querySelector("#comment");
                ele.scrollIntoView(true); // true 是默认的
            },
            store() { // 收藏
                articleApi.addCollect({token:getLocalStorage('token'),article_id:this.article.article_id}).then(res => {
                    console.log(res)
                    this.article.collect_flag = res.collect_flag
                    if(this.article.collect_flag) {
                        console.log('取消收藏')
                        this.store_name = '取消收藏';
                    }else{
                        console.log('收藏')
                        this.store_name = '收藏'
                    };
                })
            },
            point() { // 点赞
                articleApi.addLikes({token:getLocalStorage('token'),article_id:this.article.article_id}).then(res => {
                    console.log(res)
                    this.article.point_flag = res.point_flag
                    this.article.point_count = res.point_count
                    if(this.article.point_flag) {
                        console.log('取消点赞')
                        this.point_name = '取消点赞';
                    }else{
                        console.log('点赞')
                        this.point_name = '点赞'
                    };
                })
            },
            chat(id) { // 私信
                let routeUrl = this.$router.resolve({
                    path:'/message',
                    query:{id:id}
                })
                window.open(routeUrl.href,"_blank")
            },
            userinfo(id) {
                this.$router.push({path:'/userinfo', query: {id:id}})
            },
        },
        created(){
            articleApi.getDetailInfo({
                article_id: this.$route.query.id,
                token: getLocalStorage('token')}
            ).then(res => {
                console.log(res);
                this.article = res.article;
                this.user = res.user;
                // console.log(this.article);
                // console.log(this.user);
                if(this.article.collect_flag) this.store_name = '取消收藏';
                else this.store_name = '收藏';
                if(this.article.point_flag) this.point_name = '取消点赞';
                else this.point_name = '点赞';

            })
        },
        components: {
            Nav,
            comment
        }
    }
</script>

<style lang="scss" scoped>
    .main{
        width: 1000px;
        height: 1000px;
        margin: 10px auto;
    }
    .el-button {
        padding: 10px 20px;
    }
    .article_icon {
        font-size: 15px;
        color: #909399;
        vertical-align: middle;
        margin-left: 10px;
    }
    .title_main {
        width: 940px;
        margin: 10px auto;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
        padding: 20px 30px;
        position: relative;
        .title {
            font-size: 22px;
            font-weight: 600;
            width: 75%;
        }
        .tags {
            margin: 10px 0px 20px 0px;
            .el-tag {
                margin-right: 5px;
            }
        }
        .hot_info {
            position: absolute;
            top: 20px;
            right: 30px;
            width: 200px;
            .hot_title {
                font-size: 14px;
                color: #8590a6;
                margin-bottom: 5px;
            }
            strong {
                font-size: 18px;
                font-weight: 600;
            }
            .star_account {
                display: inline-block;
                border-right: 1px solid #ebebeb;
                padding-right: 10px;
                text-align:center;
            }
            .comment_account {
                display: inline-block;
                padding-left: 10px;
                text-align:center;
            }
        }
    }
    .article_main{
        display: inline-block;
        width: 670px;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
        padding: 50px 30px;
        font-size: 15px;
        line-height: 1.5;
        word-break: break-word;
        .article_time {
            margin: 10px 0px;
            color:#909399;
        }
        .article_icon {
            margin-right: 10px;
            margin-left: 0px;
        }
        .like_btn {
            float: right;
        }
        .article_content /deep/ img {
            max-width: 90%;
            height: auto;
            display: block;
        }
        .article_content /deep/ video {
        width: 90% !important;
        height:auto;
        margin:auto;
        display:block;
    }
    }
    .user_main{
        float: right;
        width: 260px;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
        .user_title {
            height: 50px;
            text-align: center;
            line-height: 50px;
            font-size: 15px;
            font-weight: 600;
        }
        .user_info {
            border-top: 1px solid #ebebeb;
            padding: 15px;
            .user_avatar {
                cursor: pointer;
                width: 60px;
                height: 60px;
            }
            .user_name {
                cursor: pointer;
                display: inline-block;
                font-size: 15px;
                font-weight: 600;
                margin-left: 10px;
            }
            .level_name {
                margin-left:5px;
                color: #8DAFFC;
            }
            .user_like {
                border-top: 1px solid #ebebeb;
                margin-top: 15px;
                padding-top: 15px;
                text-align: center;
                .hot_title {
                    font-size: 14px;
                    color: #8590a6;
                    margin-bottom: 5px;
                }
                strong {
                    font-size: 18px;
                    font-weight: 600;
                }
                .article {
                    display: inline-block;
                    border-right: 1px solid #ebebeb;
                    padding-right: 20px;
                    text-align:center;
                }
                .collection {
                    display: inline-block;
                    border-right: 1px solid #ebebeb;
                    padding: 0px 20px;
                    text-align:center;
                }
                .credit {
                    display: inline-block;
                    padding-left: 20px;
                    text-align:center;
                }

            }
            .chat_btn {
                margin-top: 15px;
                width: 230px;
            }
        }
    }
    .comment_main {
        width: 670px;
        margin-top: 10px;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
        padding: 50px 30px 40px 30px;
    }
</style>
