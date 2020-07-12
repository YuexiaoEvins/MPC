<template>
    <div>
        <Nav></Nav>
        <div class="index_container">
            <div class="main1">
                <el-menu :default-active="$route.path"  class="el-menu-demo" mode="horizontal"  router>
                    <el-menu-item index="/hotPoint" class="index_nav" >热榜</el-menu-item>
                    <el-menu-item index="/follow" class="index_nav">留言板</el-menu-item>
<!--                    <el-menu-item @click="goEditBlog" class="editBlog"><el-button class="el-icon-plus">写博客</el-button></el-menu-item>-->
                </el-menu>
                <el-divider></el-divider>
                <router-view></router-view>
            </div>
            <div style="display: flex;flex-direction: column;">
                <div class="side_bar" style="height: 80px">
                   <div class="slide_bar_item" @click="$router.push('/editBlog')"><p class="iconfont iconwenzhang1 icon_draft" ></p>写文章</div>
                   <div class="slide_bar_item" @click="$router.push('/draft')"><p class="iconfont iconcaogaoxiang icon_draft" ></p>草稿箱</div>
                </div>
                <div class="side_bar" style="top:170px">
                    <div class="slide_bar_item" @click="goToClass('1001')"><p class="iconfont iconWEBqianduan icon_fontend" ></p><span>前端</span></div>
                    <div class="slide_bar_item" @click="goToClass('1002')"><p class="iconfont iconapphoutaiguanli icon_backend"></p>后端</div>
                    <div class="slide_bar_item" @click="goToClass('1003')"><p class="iconfont iconshouji icon_mobile" ></p>移动端</div>
                    <div class="slide_bar_item" @click="goToClass('1004')"><p class="iconfont iconfuwuqi icon_server" ></p>服务器</div>
                    <div class="slide_bar_item" @click="goToClass('1005')"><p class="iconfont iconhuabanfuben icon_operation" ></p>运营</div>
                    <div class="slide_bar_item" @click="goToClass('1006')"><p class="iconfont iconchanpin icon_product" ></p>产品</div>
                    <div class="slide_bar_item" @click="goToClass('1007')"><p class="iconfont iconceshi icon_test" ></p>测试</div>
                    <div class="slide_bar_item" @click="goToClass('1008')"><p class="iconfont iconicon4 icon_design" ></p>设计</div>
                    <div class="slide_bar_item" @click="goToClass('1009')"><p class="iconfont iconicon-test icon_else" ></p>其他</div>
                </div>
                <div class="side_bar" style="top:410px;height: 235px">
                    <div class="searchContainer">
                        <p class="popular">热搜榜</p>
                        <p v-if="popular.length == 0 " class="no_popular">暂无热搜~</p>
                        <p class="popular_item" v-for="(item,index) in popular" :key="index" @click="goSearch(item.keyword)" v-else>{{item.keyword}} <span class="iconfont iconhuo" style="color: #ff3204"></span></p>
                    </div>
                </div>
                <div class="side_bar_img" >
                    <div class="block" style="height: 125px;width:240px">
                        <el-carousel trigger="click" height="135px">
                            <el-carousel-item v-for="(item,index) in advanPhoto" :key="index">
                                <img :src="item" alt="" class="advan_img">
                            </el-carousel-item>
                        </el-carousel>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import Nav from '../../components/navBar/nav'
    import api from "../../api/article";
    import {getLocalStorage} from "../../utils/auth";

    export default {
        name: "index",
        data(){
            return{
                activeName: 'first',
                isActived:false,
                data:[],
                popular:[],
                advanPhoto:[]
            }
        },
        created(){
            api.popularSearch({token:getLocalStorage('token')}).then(res =>{
                this.popular = res.search
            });
            api.getIndexAd().then(res => {
                console.log(res)
               this.advanPhoto = res.advertise
            })
        },
        methods: {
            goToClass(val){
                this.$router.push({path:'/classification',query:{id:val}})
            },
            goSearch(word){
                var route = this.$router.resolve({
                    path:'/searchResult',
                    query:{
                        q:word
                    }
                })
                window.open(route.href,'_blank')
            },
        },
        components:{
            Nav
        }
    }
</script>

<style lang="scss" scoped>
    .index_container {
        display: flex;
        width: 1000px;
        justify-content: center;
        position: relative;
        margin: 10px auto;
        left: -135px;
        .main1{
            position: relative;
            width: 730px;
            min-height: 950px;
            margin-right: 20px;
            background-color: #ffffff;
            box-shadow: 0 0px 15px rgba(26,26,26,.1);
            border-radius: 5px;
            .editBlog{
                float: right;
            }
            .index_nav{
                margin-left: 15px;
                font-size:15px;
                font-weight: 600;
            }
            .el-menu-item {
                border: 0;
            }
            .el-divider {
                margin-top: 0px;
            }
        }
        .side_bar{
            min-width: 250px;
            max-width: 250px;
            background-color: #ffffff;
            height: 225px;
            // margin-top: 15px;
            box-shadow: 0 0px 15px rgba(26,26,26,.1);
            border-radius: 5px;
            position: fixed;
            top: 73px;
            padding: 15px;
            box-sizing: border-box;
            display: flex;
            flex-wrap:wrap;
            justify-content: space-around;
            .searchContainer{
                display: block;
                width: 250px;
                padding: 0;
                .popular{
                    border-bottom: 1px solid #cbd7ec;
                    height: 40px;
                    line-height: 40px;
                    color: #8590a6;
                    font-size: 15px;
                    font-weight: normal;
                    margin-top: -15px;
                    position: relative;
                }
                .popular_item{
                    color:#1a1a1a;
                    font-size: 15px;
                    font-weight: normal;
                    height: 35px;
                    line-height: 35px;
                    cursor: pointer;
                    padding: 0 15px ;
                }
                .no_popular{
                    text-align: center;
                    color: #8590a6;
                    font-size: 15px;
                    margin-top: 15px;
                }
            }
            &_img{
                min-width: 250px;
                max-width: 250px;
                background-color: #ffffff;
                height: 135px;
                margin-top: 15px;
                position: fixed;
                box-shadow: 0 0px 15px rgba(26,26,26,.1);
                border-radius: 5px;
                top: 645px;
                padding: 0px;
                box-sizing: border-box;
                display: flex;
                flex-wrap:wrap;
                justify-content: space-around;
                align-items: center;
                .advan_img{
                    width: 240px;
                    height: 126px;
                    border-radius: 8px;
                }
            }
            .slide_bar_item{
                display: inline-block;
                text-align: center;
                color:#444;
                height: 60px;
                width: 60px;
                font-size: 15px;
                font-weight:400;
                cursor: pointer;
            }
            .icon{
                &_draft{
                    font-size: 20px;
                }
                &_fontend{
                    color: #fd992a;
                    font-size: 20px;
                }
                &_backend{
                    color: #42acfd;
                    font-size: 20px;
                }
                &_mobile{
                    color: rgb(255, 207, 0);
                    font-size: 20px;
                    font-weight: 600;
                }
                &_server{
                    color: rgb(67, 212, 128);
                    font-size: 20px;
                }
                &_operation{
                    color: rgb(131, 121, 212);
                    font-size: 20px;
                }
                &_product{
                    color: rgb(0, 201, 212);
                    font-size: 20px;
                }
                &_test{
                    color: rgb(212, 102, 3);
                    font-size: 20px;
                }
                &_design{
                    color: rgb(212, 85, 185);
                    font-size: 20px;
                }
                &_else{
                    color: rgb(166, 61, 20);
                    font-size: 20px;
                }
            }
        }
    }


</style>
