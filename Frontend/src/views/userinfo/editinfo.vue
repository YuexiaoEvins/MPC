<template>
    <div>
        <Nav style="position:sticky;"></Nav>
        <div class="main">
            <div class="info_edit">
                <el-upload
                    class="avatar-uploader"
                    action="string"
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="imgchange"
                    >
                    <img :src="form.user_url" class="avatar">
                    <i class="el-icon-camera-solid avatar-uploader-icon"><span>修改头像</span></i>
                </el-upload>
                <el-form  class="userinfo-form" ref="form" :model="form" label-width="50px">
                    <el-form-item label="昵称">
                        <el-input v-model="form.user_name"></el-input>
                    </el-form-item>
                    <el-form-item label="性别">
                        <el-radio-group v-model="form.user_gender">
                            <el-radio :label="1">男</el-radio>
                            <el-radio :label="0">女</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="电话">
                        <el-input v-model="form.user_phone"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱">
                        <el-input v-model="form.email"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button class="edit_btn" icon="el-icon-edit" @click="resetPsw">修改密码</el-button>
                        <el-button type="primary" @click="onSubmit">确定</el-button>
                        <el-button @click="back">取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import Nav from '../../components/navBar/nav'
    import api from '../../api/user'
    import {getLocalStorage} from "../../utils/auth";
    import {setLocalStorage} from "../../utils/auth";

    export default {
        name: "editinfo",
        data(){
            return {
                form: {
                    token: getLocalStorage('token'),
                    user_id: getLocalStorage('user_id'),
                    user_name: getLocalStorage('user_name'),
                    user_url: getLocalStorage('user_url'),
                    user_phone: getLocalStorage('user_phone'),
                    email: getLocalStorage('email'),
                    user_gender:getLocalStorage('user_gender'),
                },
            }
        },
        methods: {
            imgchange(file) {
                const isJPG = file.raw.type === 'image/jpeg';
                const isLt2M = file.raw.size / 1024 / 1024 < 2;

                if (!isLt2M) {
                    this.$message.error('上传头像图片大小不能超过 2MB!');
                    return
                }
                let formData = new FormData();
                formData.append('profile_photo', file.raw);
                formData.append('token', getLocalStorage('token'));
                formData.append('user_id', getLocalStorage('user_id'));
                console.log(formData.getAll('profile_photo'))
                api.uploadPhoto(formData).then(res => {
                    this.form.user_url = res.url;
                    console.log(this.form.user_url);
                    });
            },
            resetPsw() {
                this.$router.push('/editpsw');
            },
            back() {
                this.$router.back();
            },
            onSubmit() {
                let formData = new FormData();
                for ( let item in this.form) {
                    formData.append(item, this.form[item]);
                }
                api.editUserInfo(formData).then(res => {
                    console.log(res);
                    setLocalStorage('user_name', this.form.user_name),
                    setLocalStorage('user_phone', this.form.user_phone),
                    setLocalStorage('email', this.form.email),
                    setLocalStorage('user_gender', this.form.user_gender),
                    setLocalStorage('user_url', this.form.user_url)

                    this.$router.push('/userinfo');

                });
            },
        },
        created(){

        },
        components: {
            Nav
        }
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
    .avatar-uploader{
        margin-bottom: 10px;
        /deep/ .el-upload {
            border: 2px solid #fff;
            border-radius: 6px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .el-upload:hover {
            border-color: #8DAFFC;
        }
    }
    .avatar-uploader-icon {
        font-size: 30px;
        color: #8c939d;
        width: 178px;
        height: 178px;
        line-height: 178px;
        text-align: center;
        position: absolute;
        z-index: 999999;
        top: 0px;
        left: 0px;
        background-color: #1a1a1a;
        opacity: .4;
        span {
            position: absolute;
            font-size: 15px;
            top: 26px;
            left: 60px;
        }
    }
    .avatar {
        width: 178px;
        height: 178px;
        display: block;
    }
</style>
