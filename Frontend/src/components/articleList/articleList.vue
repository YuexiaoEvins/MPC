<template>
    <div>
        <div class="article_list" >
            <img :src="item.user.user_url" class="article_avatar">
            <div class="article_time_name">
                <span class="article_name">{{item.user.user_name}}</span>
                <i class="el-icon-medal level_name">{{ item.level_name }}</i>
                <p class="article_time">{{item.create_time}}</p>
            </div>
            <p class="article_title">
                <span @click="goArticle(item.article_id)">{{item.title}}</span>
                <el-tag style="float: right" v-if="item.type_name">{{item.type_name}}</el-tag>
            </p>
            <!--缩略文章-->
            <div class="picture_content" v-show="!showAticle">
                <div class="article_picture" @click="goArticle(item.article_id)" v-show="item.photo.photo_url != null">
                    <span class="iconfont iconbofang video_play" v-if="item.photo.photo_flag == 3"></span>
                    <img :src="item.photo.photo_url" style="width: 250px" >
                </div>
                <p class="article_content" ><span @click="goArticle(item.article_id)">{{item.simple_content | articleFilter}}</span>
                    <span class="readMore" @click="readMore(item.article_id)">阅读全文 <span class="iconfont iconjiantouyou control"></span></span>
                </p>
            </div >
            <!--完整文章-->
            <div v-if="showAticle">
                <div class="full_article" >
                    <p v-html="FullArticle">
                    </p>
                    <span class="readMore" @click="hideFullArticle(index)">收起 <span class="iconfont iconjiantoushang control"></span></span>
                </div>
            </div>
            <!--展示评论-->
            <span class="iconfont iconpinglun common" @click="openComment(item.article_id)">{{!showComment ? (item.comment_count > 0 ?item.comment_count: 0 )  + '条': '收起'}}评论</span>
            <span class="common animation" :class="[item.collect_flag > 0 ? 'isCollect_active':'common']" @click="collectArticle(name,item.title,'collect',item.user.user_id,item.article_id)"> <span class="iconfont iconxingxing animation"></span> {{item.collect_flag >0?'已':''}}收藏</span>
            <span  :class="[item.point_flag > 0 ? 'islike_active':'common']" @click="addLikes(name,item.title,'like',item.user.user_id,item.article_id)"><span class="iconfont  icondianzan animation"></span>{{item.point_flag>0?'已':''}}点赞{{'  '+item.point_count}}</span>
            <span class="common page_view" >{{item.page_view}}阅读数</span>
            <div v-if="showComment" class="showComment">
                <comment :article_id="article_id"></comment>
            </div>
            <el-divider></el-divider>
        </div>
    </div>
</template>

<script>
    import api from '../../api/article'
    import comment from "../../components/comment/comment";
    import {getLocalStorage} from "../../utils/auth";
    import {EventBus} from "../../api/busEvent";

    export default {
        name: "articleList",
        props:["item"],
        data(){
            return{
                showAticle:false,
                showComment:false,
                FullArticle:'',
                article_id:'',
                userId:getLocalStorage('user_id'),
                name:getLocalStorage('user_name')
            }
        },
        methods:{

            readMore(id) {
                api.getFullArticle({article_id:id,token:getLocalStorage('token')}).then(res => this.FullArticle = res.content)
                this.showAticle = !this.showAticle
            },
            goArticle(id){
                let routeUrl = this.$router.resolve({
                    path:'/articleDetail',
                    query:{id:id}
                })
                window.open(routeUrl.href,"_blank")
            },
            openComment(id){
                this.article_id = id
                // console.log(this.article_id)
                this.showComment = ! this.showComment
            },
            addLikes(name,val,type,id,article_id){   //点赞函数
                api.addLikes({token:getLocalStorage('token'),article_id:article_id}).then(res =>{
                    // console.log(res)
                    this.item.point_flag = res.point_flag
                    this.item.point_count = res.point_count
                    if(res.point_flag > 0){
                        EventBus.$emit('sentMqtt',`${val + "*&^*&^" +name + "*&^*&^" + type}`,id)
                    }
                    console.log('点赞成功')
                })
            },
            hideFullArticle(){
                this.showAticle = !this.showAticle
            },
            collectArticle(name,val,type,id,article_id){ //收藏函数
                api.addCollect({token:getLocalStorage('token'),article_id:article_id}).then(res =>{
                    // console.log(res)
                    this.item.collect_flag = res.collect_flag
                    if (res.collect_flag > 0){
                        EventBus.$emit('sentMqtt',`${val + "*&^*&^" +name + "*&^*&^" + type}`,id)
                    }
                    console.log('收藏成功')
                })
            }
        },
        computed:{

        },
        filters:{
            articleFilter(content){
                return content + '...'
            }
        },
        components:{
            comment
        },
        mounted() {
            EventBus.$on('resetFlag',(val)=> {
                this.showAticle = false;
                this.showComment = false;
            })
        }
    }
</script>

<style lang="scss" scoped>
    /*@keyframes scale {*/
    /*    0%{*/
    /*        transform: scale(1);*/
    /*    }*/
    /*    25%{*/
    /*        transform: scale(0.5);*/
    /*    }*/
    /*    50%{*/
    /*        transform: scale(1);*/
    /*    }*/
    /*    75%{*/
    /*        transform: scale(1.5);*/
    /*    }*/
    /*    100%{*/
    /*         transform: scale(1);*/
    /*     }*/
    /*}*/
    .article_list{
        width:100%;
        margin: 0px auto;
    .article_avatar{
        width: 60px;
        height: 60px;
        margin-left: 20px;
    }
    .article_time_name{
        display: inline-block;
        height: 60px;
        position: relative;
        top:18px;
        margin-left: 15px;
        .article_name{
            font-size: 18px;
        }
        .article_time{
            color: #6d6d6d;
            font-size: 12px;
        }
        .level_name {
            margin-left:5px;
            color: #8DAFFC;
        }
    }
    .article_title{
        font-size: 18px;
        font-weight: 600;
        margin: 20px;
        cursor: pointer;
    span{
    &:hover{
         color:#75a7d6;
         cursor: pointer;
     }
    }
    .el-tag {
        margin-left: 5px;
        font-weight: 400;
        //margin-right: 10px;
    }
    }
    .picture_content{
        display: flex;
        justify-content: center;
        padding: 0 20px;
        .readMore{
            color:#175199;
            font-weight: 600;
            font-size: 14px;
            margin-left: 5px;
        }
    .article_picture{
        width: 190px;
        height: 105px;
        border-radius: 8px;
        margin: 0 15px 15px 0;
        cursor: pointer;
        overflow: hidden;
        position: relative;
        img{
            position: absolute;
            z-index: 0;
            top:50%;
            left:50%;
            transform: translate(-50%,-50%);
            user-select: none
        }
        .video_play{
            width: 43px;
            display: inline-block;
            height: 43px;
            background-color: rgb(255, 255, 255);
            border-radius: 50%;
            font-size: 39px;
            text-align: center;
            position:absolute;
            color: rgba(0, 0, 0, 1);
            top:50%;
            left:50%;
            transform: translate(-50%,-50%);
            z-index: 1;
        }
    }
    .article_content{
        margin-bottom: 25px;
        font-size: 15px;
        display: inline-block;
        margin-top: 0px;
        width: 600px;
        flex: 1;
        >span:hover{
            color:#175199;
            cursor: pointer;
        }
    }
    }
    .full_article{
        padding: 0px 20px 8px 20px;
        position: relative;
        overflow: hidden;
        img{
            width: 85%!important;
        }
        .readMore{
            color:#8590a6;
            font-size: 12px;
            font-weight:600;
            cursor: pointer;
            float: right;
            margin: 10px 5px 0px 0px;
        }
    }
    .full_article /deep/ img {
        max-width: 90%;
        height: auto;
        display: block;
    }
    .full_article /deep/ video {
        width: 90% !important;
        height: fit-content;
        margin:auto;
        display:block;
    }
    .control {
        font-size: 12px;
    }
    .common{
        color:#8590a6;
        margin: 0 20px;
        cursor: pointer;
        font-size: 14px;
        user-select: none;
        /*.animation{*/
        /*    animation: scale 0.5s;*/
        /*}*/
    }

    .islike_active{
        color: #ff6535;
        margin: 0 15px;
        cursor: pointer;
        font-size: 14px;
        user-select: none;
    }
    .isCollect_active{
       color: #e9b91f;
       margin: 0 15px;
       cursor: pointer;
       font-size: 14px;
       user-select: none;
    }
    .page_view{
        float: right;
        margin-right: 25px;
        cursor: auto;
    }
    .showComment{
        width: 90%;
        box-shadow: 0 0px 15px rgba(26, 26, 26, 0.1);
        border-radius: 5px;
        margin: 10px auto;
        padding: 10px 15px 25px 15px;
        margin-bottom: 25px ;
     }
    }
</style>
