<template>
    <div class="register_page">
        <div class="register_container">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm register_input">
                <el-form-item label="密码" prop="pass">
                    <el-input type="password" v-model="ruleForm.pass" autocomplete="off" prefix-icon="el-icon-link" show-password placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                    <el-input type="password" @keyup.enter.native="submit" v-model="ruleForm.checkPass" autocomplete="off" prefix-icon="el-icon-link" show-password placeholder="再次输入密码"></el-input>
                    <el-button type="primary"  @click="submitForm('ruleForm')" class="resetBtn">重置密码</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    import api from '../../api/user'
    // import { getLocalStorage } from '../../utils/auth'
    export default {
        name: "login",
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                }else if (value.length < 6){
                    callback(new Error('密码不能低于6位数'))
                } else {
                    if (this.ruleForm.checkPass !== '') {
                        this.$refs.ruleForm.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.ruleForm.pass) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                ruleForm: {
                    pass: '',
                    checkPass:'',
                },
                token:'',
                sendflag:false,
                computedTime:0,
                rules: {
                    pass: [
                        { validator: validatePass, trigger: 'blur' ,required: true}
                    ],
                    checkPass: [
                        { validator: validatePass2, trigger: 'blur' ,required: true}
                    ],
                }
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        api.changepasswd({
                            token:this.token,
                            password:this.ruleForm.pass,
                            re_password:this.ruleForm.checkPass
                        }).then(res => {
                            if (res.code == 200){
                                this.$router.replace({path:'/login'})
                            }else if(res.code == 401){
                                this.$message.error('用户不存在')
                            }else{
                                this.$message.error('修改失败')
                            }
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            sendCode(){
                this.sendflag = true
                this.computedTime = 30
                var timer = setInterval(() => {
                    this.sendflag = false
                    clearInterval(timer)
                },30000)
                var computedTimer = setInterval(()=>{
                    if(this.computedTime > 0 ){
                        this.computedTime --
                    }else{
                        clearInterval(computedTimer)
                    }
                },1000)
            },
            submit(){
                console.log('敲空格了')
            }
        },
        created() {
         var arr =  window.location.hash.split('?')
         var arr2 = arr[arr.length-1].split('=')
         this.token = arr2[arr.length-1]
        }
    }
</script>

<style lang="scss" >
    .register_page{
        position: relative;
        background-image: url("http://pic.90sjimg.com/design/01/34/58/13/58dcfe0be8011.png") ;
        background-size:100% 100%;
        width: 100%;
        height: 100vh;
        .register_container{
            width: 370px;
            background-color: rgba(38,38,38,0.35);
            height: 100vh;
            position: absolute;
            top:0px;
            left: 100%;
            transform: translate(-100%,0);
            box-shadow: 0 0 10px 10px #f3f3f3;
            /*border-radius: 8px;*/
        }
        .register_input{
            width: 350px;
            position: absolute;
            left: 0%;
            top:35%;
            .resetBtn{
                margin-top: 8px;
                width: 250px;
            }
            .el-form-item__label{
                color:#fff;
            }

        }
    }
</style>

<style lang="scss" >
    .login_page{
        position: relative;
        background-color: #eee;
        background-image: url("https://img.zcool.cn/community/0154d25d5c96d7a8012187f4f9aa4c.jpg@1280w_1l_0o_100sh.jpg")  ;
        background-size:100% 100%;
        background-repeat:no-repeat;
        width: 100%;
        height: 890px;
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
            .login_btn{
                width: 300px;
                margin-left:60px;
            }
            .login_input{
                width: 350px;
                margin-left: -50px;
                color:#fff;
                .el-form-item__label{
                    color:#fff;
                }
            }
        }
    }
</style>
