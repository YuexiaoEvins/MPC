<template>
    <div class="register_page">
        <div class="register_container">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm register_input">
                <el-form-item label="昵称" prop="name">
                    <el-input v-model="ruleForm.name" placeholder="你的昵称"></el-input>
                </el-form-item>
                <el-form-item label="工号" prop="account">
                    <el-input v-model="ruleForm.account" placeholder="你的工号"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email"  :rules="[
                  { required: true, message: '请输入邮箱地址', trigger: 'blur' },
                  { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
                ]">
                    <el-input v-model="ruleForm.email" prefix-icon="el-icon-message" placeholder="请输入邮箱"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                    <el-input type="password" v-model="ruleForm.pass" autocomplete="off" prefix-icon="el-icon-link" show-password placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                    <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off" prefix-icon="el-icon-link" show-password placeholder="再次输入密码"></el-input>
                    <span class="register" @click="$router.push({path:'/login'})">返回登陆</span>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="snowMask"></div>
    </div>
</template>

<script>
    import api from '../../api/user'
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
                    email: '',
                    checkPass:'',
                    name:'',
                    account:''
                },

                verCode:'',
                sendflag:false,
                computedTime:0,
                rules: {
                    pass: [
                        { validator: validatePass, trigger: 'blur' ,required: true}
                    ],
                    checkPass: [
                        { validator: validatePass2, trigger: 'blur' ,required: true}
                    ],
                    email: '',
                    name: [
                        { required: true, message: '请输入昵称', trigger: 'blur' },
                        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                    ],
                    account: [
                        { required: true, message: '请输入工号', trigger: 'blur' },
                        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                    ]
                }
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        api.register({
                            email:this.ruleForm.email,
                            password:this.ruleForm.pass,
                            user_name:this.ruleForm.name,
                            user_account:this.ruleForm.account
                        }).then(res =>{
                        if(res.code == 200 ){
                            this.$message.success('注册成功');
                            this.$router.push({path:'/login'})
                        }else if(res.code == 401){
                            this.$message.error('该账号已存在')
                        }else{
                            this.$message.error('注册失败')
                        }
                        }
                        )
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
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
            }
        }
    }
</script>

<style lang="scss" >
    .register_page{
        position: relative;
        background-image: url("../../assets/注册.png") ;
        background-size:100% 100%;
        width: 100%;
        height: 884px;
        .register_container{
            background-color: rgba(38,38,38,0.35);
            width: 600px;
            height: 420px;
            position: absolute;
            top:200px;
            left: 50%;
            padding: 42px 0px 20px 0px;
            transform: translate(-50%,0);
            box-shadow: 0 0 5px 5px #e6e6e6;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .register_input{
            width: 350px;
            .register{
                color:#fff;
                font-weight: bold;
                cursor:pointer;
            }
            .el-form-item__label{
                color:#fff;
            }
            .register_verCode{
                width: 120px;
            }
            .register_btn{
               margin-left: 15px;
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
