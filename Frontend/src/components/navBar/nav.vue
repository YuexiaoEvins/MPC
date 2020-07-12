<template>
    <div style="z-index: 99;position: sticky;top: 0">
          <div class="nav">
             <div class="com">
                    <div class="nav_logo" @click="$router.push('/')"><img src="../../assets/logo.jpg" class="nav_logo_pic"></div>
                    <div class="nav_menu">
                        <el-menu :default-active="$route.path" class="el-menu-demo" mode="horizontal" router>
                            <el-menu-item index="/" >首页</el-menu-item>
                            <el-menu-item index="/classification" >兴趣</el-menu-item>
                            <el-input class="search"
                                      v-model="state"
                                      prefix-icon="el-icon-search"
                                      placeholder="请输入内容"
                                      @select="handleSelect"
                                      @focus="focus"
                                      @blur="blur"
                                      @keyup.enter.native="search"></el-input>
                            <el-button type="primary" class="searchBtn" @click="search">搜索</el-button>
                            <div class="nav_user">
                                <img class="user_avatar" :src="user_url">
                                <div class="user_panel" >
                                    <p class="user_name">
                                        {{userInfo.user_name}} <span :class="[userInfo.gender > 0 ?'el-icon-male':'el-icon-female']"></span>
                                    </p>
                                    <p class="user_level"><i class="el-icon-trophy level_name">{{ userInfo.user_level_name }}</i></p>
                                    <div class="get_user_nums">
                                        <div class="nums_item">
                                            <p>文章数</p>
                                            <span>{{userInfo.user_write_count}}</span>
                                        </div>
                                        <div class="nums_item">
                                            <p>获赞数</p>
                                            <span>{{userInfo.user_point}}</span>
                                        </div>
                                        <div class="nums_item">
                                            <p>收藏数</p>
                                            <span>{{userInfo.user_collect_count}}</span>
                                        </div>
                                    </div>
                                    <div  class="user_item user_border">
                                        <span class="iconfont iconziyuanxhdpi "></span>{{userInfo.user_account}}
                                        <span class="iconfont iconjifen credit"></span>积分:{{userInfo.user_credit}}
                                    </div>
                                    <router-link class="use_info" to="/userinfo" tag="div"><span class="iconfont iconyonghu"></span>个人主页</router-link>
                                    <div class="user_item"><span class="iconfont iconshouji">：{{userInfo.user_phone}}</span></div>
                                    <div class="user_item"><span class="iconfont iconyouxiang">：{{userInfo.email}}</span></div>
                                    <router-link class="use_info user_border_top" to="/login" @click.native="clearStorage" tag="div"><span class="iconfont icontuichu2"></span>退出</router-link>
                                </div>
                            </div>
                            <div class="nav_message">
                                <router-link to="/message"><i class="el-icon-chat-dot-round"></i></router-link>
                            </div>
                        </el-menu>
                        <transition name="fade">
                            <div class="searchContainer" v-show="isSearch">
                                <p class="popular">热词搜索</p>
                                <p class="popular_item" v-for="(item,index) in popularWord" :key="index" @click="goSearch(item.keyword)">{{item.keyword}} <span class="iconfont iconhuo" style="color:#ff3204 "></span></p>
                                <p class="popular">搜索记录 <span class="el-icon-delete-solid deleteHis" @click="deleteAllHis">清空</span></p>
                                <p class="popular_item" v-for="(item,index) in historyWord" :key="index" @click="goSearch(item.word)">{{item.word}} <span class="el-icon-close deleteOneHis" @click.stop="deleteOneHis(index,item.word)"></span></p>
                            </div>
                        </transition>
                    </div>

                </div>
        </div>

    </div>
</template>

<script>
    import {getLocalStorage} from "../../utils/auth";
    import api from '../../api/article'
    import search from "../../api/search";
    import user from '../../api/user'
    export default {
        name: "nav",
        data(){
            return{
                activeIndex: '/',
                // userData: null,
                isActived:true,
                user_url: getLocalStorage('user_url'),
                state: '',
                popular:[],
                isSearch:false,
                popularWord: [],
                historyWord:[],
                userInfo:[]
            }
        },
        created(){
           user.getUserInfo({token:getLocalStorage('token'),user_id:getLocalStorage('user_id')}).then(res =>{
              this.userInfo = res.user
               console.log(res.user)
           })
        },
        methods:{
            clearStorage(){
                localStorage.clear()
            },
            handleSelect(item) {
                console.log(item);
            },

            focus(){
                api.popularSearch({token:getLocalStorage('token')}).then(res => {
                    this.isSearch = true
                    console.log(res)
                    this.popularWord = res.search
                    this.historyWord = res.history
                })
            },
            blur(){
                this.isSearch = false
            },
            search(){
              var route = this.$router.resolve({
                  path:'/searchResult',
                  query:{
                      q:this.state
                  }
              })
                window.open(route.href,'_blank')
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
            deleteAllHis(){
                console.log('deleteAll')
                search.deleteAllHis({token:getLocalStorage('token')}).then(res =>{
                    console.log(res)
                    this.historyWord = []
                }).catch(err =>{
                    this.$message.error('服务器错误')
                })
            },
            deleteOneHis(index,word){
                search.deleteOneHis({
                    token:getLocalStorage('token'),
                    word:word
                }).then(res =>{
                    console.log(res)
                    this.historyWord.splice(index,1)
                }).catch(err =>{
                    this.$message.error('服务器错误')
                })

            }
        }
    }
</script>

<style lang="scss" scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to {
        opacity: 0;
    }
    .searchContainer{
        width: 296px;
        min-height: 200px;
        background-color: #fff;
        z-index: 99999;
        position: absolute;
        left:24.9%;
        border-radius: 5px;
        box-shadow: 0 0 5px #bcbcbc;
        .popular{
            border-bottom: 1px solid #cbd7ec;
            height: 40px;
            line-height: 40px;
            color: #8590a6;
            font-weight: normal;
            padding: 0 15px ;
            position: relative;
            .deleteHis{
               float: right;
               margin-top: 15px;
               cursor: pointer;
            }
        }
        .popular_item{
            color:#1a1a1a;
            font-size: 15px;
            font-weight: normal;
            height: 35px;
            line-height: 35px;
            cursor: pointer;
            padding: 0 15px ;
            &:hover{
                background-color: #eee;
            }
            .deleteOneHis{
                display: inline-block;
                float: right;
                margin-top: 10px;
                cursor: pointer;
            }
        }
    }
    .nav {
        position: sticky;
        top: 0;
        box-sizing: border-box;
        z-index: 999;
        min-width: 1032px;
        height: 63px;
        background-color: #fff;
        border-bottom: 1px solid #e6e6e6;
        .searchBtn{
            margin:0px 10px;
            position: relative;
            top:12px;
        }
    }
    .com{
        margin: 0 auto;
        position: relative;
        width: 1000px;
        align-items: center;
        .nav_logo{
            float: left;
            margin: 5px 0px;
        }
        .nav_logo_pic{
            height: 50px;
        }
        .nav_menu{
            margin: 0px 10px;
            display: inline-block;
            font-size:15px;
            height: 60px;
            font-weight: 600;
            .search{
                margin: 0px 0 0 10px;
                width: 300px;
                position: relative;
                left: 0px;
                top:12px;
            }
        }
        .nav_message {
            float: right;
            margin: 11px 10px 11px 249px;
            font-size: 35px;
            color: #8DAFFC;
        }
        .nav_user{
            float: right;
            position: relative;
            margin: 11px 10px;
            &:hover{
                >img{
                    transform: scale(1.5) translateY(7px);
                }
                >div{
                    transition: all 0.5s;
                    visibility: visible;
                    opacity:1;
                }
            }
        }
        .nav_login{
            float: right;
            margin-right: 15px;
        }
        .nav_register{
            float: right;
            margin-right: 150px;
        }
        .user_avatar{
            width: 35px;
            height: 35px;
            border: 1px solid #99999940;
            border-radius: 50%;
            z-index: 29999;
            transition-duration:0.5s;
            position: relative;
        }
        .user_panel{
            width:250px;
            z-index: 0;
            background-color: #fff;
            position: absolute;
            transform: translateX(-42%);
            visibility: hidden;
            opacity: 0;
            transition: all 0.3s;
            border-radius: 2px;
            box-shadow: 0 0 4px #bbb;
            .get_user_nums{
                display: flex;
                flex-wrap: nowrap;
                justify-content: center;
                border-bottom: 1px solid #eee;
                width: 100%;
                .nums_item{
                    color: #636363;
                    text-align: center;
                    font-weight: normal;
                    padding:5px 15px;
                    border-right: 1px solid #a8a8a8;
                    &:last-child{
                        border-right: none;
                    }
                }

            }
            .user_border{
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-around;
            }
            .user_border_top{
                border-top: 1px solid #eee;
                margin-top: 8px;
            }
            .user_name{
                margin-top: 33px;
                font-size: 16px;
                font-weight: normal;
                text-align: center;
                margin-bottom: 14px
            }
            .user_level{
                text-align: center;
                margin-bottom: 8px;
                color: #6fa9ff;
            }
            .use_info{
                height: 30px;
                line-height: 30px;
                color: #636363;
                font-size: 16px;
                cursor: pointer;
                padding: 4px 20px;
                font-weight: normal;
                &:hover{
                    background-color: #eee;
                }
            }
            .user_item{
                height: 30px;
                line-height: 30px;
                color: #636363;
                font-size: 16px;
                padding: 4px 20px;
                font-weight: normal;
                margin: 8px 0;
                .credit{
                    font-size: 18px;
                    padding-left: 24px;
                    color: #5272ff;
                }
            }
        }
    }
</style>
