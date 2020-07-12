<template>
    <div>
        <Nav style="position:sticky;"></Nav>
        <div class="main">
            <div class="info_show">
                <div class="pic_box"><img class="pic" :src="user.user_url"></div>
                <div class="info">
                    <div class="info_title">
                        <span>{{user.user_name}}</span>
                        <i v-if="user.user_gender == 0" class="icon-sex el-icon-female"></i>
                        <i v-else class="icon-sex el-icon-male"></i>
                        <el-tag>{{ user.user_level_name }}</el-tag>
                    </div>
                    <div class="info_detail">
                        <div>工号：{{user.user_account}}</div>
                        <div>电话：{{user.user_phone}}</div>
                        <div>邮箱：{{user.email}}</div>
                        <el-button class="edit_btn" icon="el-icon-edit" @click="goEditInfo" plain v-if="user.user_id === own.id">编辑个人信息</el-button>
                    </div>
                </div>
            </div>
            <div class="article_list">
                <el-tabs type="border-card" v-model="activeName">
                    <el-tab-pane label="已发文章" name="myarticle">
                        <myarticle :curuser_id="curuser_id"></myarticle>
                    </el-tab-pane>
                    <el-tab-pane label="已发留言" name="messageboard">
                        <messageboard :curuser_id="curuser_id"></messageboard>
                    </el-tab-pane>
                    <el-tab-pane label="点赞文章" name="pointarticle">
                        <pointarticle :curuser_id="curuser_id"></pointarticle>
                    </el-tab-pane>
                    <el-tab-pane label="已发评论" name="commentarticle">
                        <commentarticle :curuser_id="curuser_id"></commentarticle>
                    </el-tab-pane>
                    <el-tab-pane label="收藏文章" name="followarticle" v-if="user.user_id === own.id">
                        <followarticle :curuser_id="curuser_id"></followarticle>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>
</template>

<script>
    import myarticle from '@/components/userinfo/myArticle'
    import followarticle from '@/components/userinfo/followArticle'
    import commentarticle from '@/components/userinfo/commentarticle'
    import pointarticle from '@/components/userinfo/pointArticle'
    import messageboard from '@/components/userinfo/messageboard'
    import Nav from '../../components/navBar/nav'
    import {getLocalStorage} from "../../utils/auth";
    import defaultAvatar from '../../assets/unlogin.png'
    import api from '../../api/user'

    export default {
        name: "userinfo",
        data(){
            return {
                activeName: 'myarticle',
                own: {
                    id: getLocalStorage('user_id'),
                    name: getLocalStorage('user_name'),
                    avatar: getLocalStorage('user_url') || defaultAvatar,
                    phone: getLocalStorage('user_phone') || '未填写...',
                    account: getLocalStorage('user_account'),
                    email: getLocalStorage('email'),
                    sex: getLocalStorage('user_gender'),
                },
                user: {},
                curuser_id: '',
            }
        },
        components: {
            'myarticle' : myarticle,
            'followarticle' : followarticle,
            'commentarticle': commentarticle,
            'pointarticle': pointarticle,
            'messageboard': messageboard,
            Nav
        },
        methods: {
            goEditInfo() {
                this.$router.push('/editinfo')
            },
        },
        created(){
            let id;
            if(this.$route.query.id) id = this.$route.query.id;
            else id = getLocalStorage('user_id');
            this.curuser_id = id;
            api.getUserInfo({
                user_id: id,
                token: getLocalStorage('token')
            }).then(res => {
                this.user = res.user;
            })
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
    .pic_box {
        width: 200px;
        height: 200px;
        border: 1px solid #e6e6e6;
        border-radius: 8%;
        float: left;
    }
    .pic {
        width: 200px;
        height: 200px;
        border-radius: 8%;
    }
    .info {
        margin-left: 240px;
        padding-top: 84px;
        .info_title {
            font-size: 26px;
            font-weight: 600;
            .icon-sex {
                margin: 0px 5px 0px 10px;
            }
            .el-tag {
                background-color: #f4f7ff;
                padding: 0 5px;
                height: 20px;
                line-height: 20px;
                font-size: 6px;
                color: #8DAFFC;
                border: 1px solid #8DAFFC;
            }
            /deep/ .el-badge__content {
                background-color: #8DAFFC;
                font-size: 6px;
                height: 12px;
                line-height: 12px;
                padding: 0 5px;
                top: 7px;
            }
        }
        .info_detail {
            position: relative;
            font-size: 14px;
            color: #909399;
            div {
                margin-top:10px;
            }
            .edit_btn {
                position: absolute;
                right: 0px;
                bottom: 0px;
                color: #8DAFFC;
                border-color: #8DAFFC;
            }
            .edit_btn:hover {
                color: #8DAFFC !important;
                border-color: #8DAFFC !important;
                background-color: #f4f7ff !important;
            }
        }
    }
    .article_list {
        margin-top: 30px;
    }
</style>
