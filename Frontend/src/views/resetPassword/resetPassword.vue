<template>
    <div class="login_page">
        <div class="login_container">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm login_input">
                <el-form-item label="邮箱" prop="email"  :rules="[
                      { required: true, message: '请输入邮箱地址', trigger: 'blur' },
                      { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
                         ]">
                    <el-input v-model="ruleForm.email" prefix-icon="el-icon-message" placeholder="请输入邮箱..."></el-input>
                </el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')" class="login_btn" :disabled="ifSend">{{computedTime>0 ? `已发送${computedTime}s` : '发送验证码'}}</el-button>
            </el-form>
        </div>

    </div>
</template>

<script>
    import api from '../../api/user'
    export default {
        name: "login",
        data() {
            return {
                ruleForm: {
                    email: '',
                },
                rules: {
                    email: '',
                },
                computedTime:0,
                ifSend:false
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        api.resetPassword(this.ruleForm).then(res =>
                            {if (1){
                                this.ifSend = true
                                this.computedTime = 30
                                var timer = setInterval(()=>{
                                    this.ifSend = false
                                    clearInterval(timer)
                                },30000)
                                var computedTimer = setInterval(()=>{
                                    if (this.computedTime > 0){
                                        this.computedTime --
                                    }else{
                                        clearInterval(computedTimer)
                                    }
                                },1000)
                            }else{
                                this.$message.error('连接超时')
                            }
                            }
                        )
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
        }
    }
</script>

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
