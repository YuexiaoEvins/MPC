<template>
    <div class="login_page">
        <div class="login_container">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm login_input">
                <el-form-item label="工号" prop="user_account" >
                    <el-input v-model="ruleForm.user_account" prefix-icon="el-icon-message" placeholder="请输入工号..."></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password" >
                    <el-input type="password" v-model.trim="ruleForm.password" autocomplete="on"  prefix-icon="el-icon-link" show-password placeholder="请输入密码...">
                    </el-input>
                </el-form-item>
                <!-- <el-form-item label="" prop="captcha_1">
                    <el-input v-model.trim="ruleForm.captcha_1" autocomplete="on" class="login_verCode" placeholder="验证码" @focus="getVercodeImg"></el-input>
                    <img class="login_verPic" @click="changeVerPic" :src="imgsrc" alt="验证码" v-if=" imgsrc!== ''">
                </el-form-item> -->
            </el-form>
            <div class="tip">
                <span class="resetPsw" @click="$router.push({path:'resetPassword'})">忘记密码？</span>
                <span class="register" @click="$router.push({path:'/register'})">注册</span>
                <el-button :loading="loading" type="primary" @click="submitForm('ruleForm')" class="login_btn">提交</el-button>
            </div>
        </div>
        <div class="snowMask"></div>
    </div>
</template>

<script>
    import api from '../../api/user'
    import {setLocalStorage} from "../../utils/auth";

    export default {
        name: "login",
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                }else if(value.length < 6 ){
                    callback(new Error('密码不能低于6位数'));
                } else {
                    if (this.ruleForm.checkPass !== '') {
                        this.$refs.ruleForm.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass1 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('工号不能为空'));
                } else {
                    callback();
                }
            };
            // var validatePass2 = (rule, value, callback) => {
            //     if (value === '') {
            //         callback(new Error('验证码不能为空'));
            //     } else {
            //         callback();
            //     }
            // };
            return {
                ruleForm: {
                    user_account: '',
                    password: '',
                    captcha_1:'',
                    hashkey: '',
                },
                isFirst: true,
                loading: false,
                imgsrc: '',
                rules: {
                    user_account: [
                        { validator: validatePass1, trigger: 'blur' ,required: true}
                    ],
                    password: [
                        { validator: validatePass, trigger: 'blur' ,required: true}
                    ],
                    // captcha_1:[
                    //     { validator: validatePass2, trigger: 'blur' ,required: true}
                    // ]
                },
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        api.login(this.ruleForm).then(res =>
                        {
                            if(res.code == '200'){
                                const data = res
                                setLocalStorage('token',data.token)
                                setLocalStorage('user_name', data.user_name)
                                setLocalStorage('user_url', data.user_url)
                                setLocalStorage('user_gender', data.user_gender)
                                setLocalStorage('user_phone', data.user_phone)
                                setLocalStorage('user_account', data.user_account)
                                setLocalStorage('user_id',data.user_id)
                                setLocalStorage('email',data.email)
                                setLocalStorage('credit',data.user_credit)
                                this.$router.replace({path:'/hotPoint'})
                            }else if(res.code == '401'){
                                this.$message.error('用户不存在')
                                return false
                            }else if(res.code == '402'){
                                this.$message.error('密码错误')
                                return false
                            }else if(res.code == '404'){
                                this.$message.error('登陆失败')
                                return false
                            }
                            // else if(res.code == '403'){
                            //     this.$message.error('验证码错误')
                            //     return false
                            // }else{
                            //     this.$message.error('服务器错误')
                            //     return false
                            // }
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            getVercodeImg() {
                if(this.isFirst) {
                    api.getVercode().then(res => {
                        console.log(res);
                        this.imgsrc = res.image_url;
                        this.ruleForm.hashkey = res.hashkey;
                    })
                    this.isFirst = false;
                }
            },
            changeVerPic(){
                this.isFirst = true;
                this.getVercodeImg();
            }
        }
    }
</script>

<style lang="scss" >
.el-input__clear{
    float: right!important;
 }
.login_page{
    position: relative;
    background-color: #eee;
    background-image: url("../../assets/登录.png")  ;
    background-size:100% 100%;
    background-repeat:no-repeat;
    width: 100%;
    height: 883px;
    .login_container{
        background-color: rgba(38,38,38,0.35);
        width: 500px;
        height: 300px;
        position: absolute;
        top:200px;
        left: 50%;
        transform: translate(-50%,0);
        box-shadow: 0 0 10px 10px #f3f3f3;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        .login_input{
            width: 350px;
            margin-left: -50px;
            color:#fff;
            .el-form-item__label{
                color:#fff;
            }
            .login_verCode{
                width: 140px;
            }
            .login_verPic{
                width: 85px;
                height: 40px;
                margin-left: 24px;
                cursor: pointer;
            }
            .iconPos{
                float: right;
            }
        }
        .tip {
            width: 300px;
            .resetPsw{
                cursor:pointer;
                color: #fff;
            }
            .register{
                color: #fff;
                float: right;
                font-weight: bold;
                cursor:pointer;
            }
            .login_btn{
                margin-top:5px;
                width: 300px;
            }
        }
    }
    @keyframes snow{
        0% {
            background-position: 0 0, 0 0;
        }
        100% {
            background-position: 500px 500px, 1000px 500px;
        }
    }
    
    .snowMask {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: url('../../assets/snow1.png'),url('../../assets/snow2.png');
        animation: 10s snow linear infinite;
        pointer-events: none;
    }
}
</style>
