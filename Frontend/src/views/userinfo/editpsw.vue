<template>
<div>
    <Nav style="position:sticky;"></Nav>
    <div class="main">
        <div class="info_edit">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">

                <el-form-item label="密码" prop="pass">
                    <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                    <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                    <el-button @click="back">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</div>
</template>

<script>
import Nav from '../../components/navBar/nav'
import {getLocalStorage} from "../../utils/auth";
import api from '../../api/user'
export default {
    name: "editinfo",
    data() {

        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else if(value.length < 6){
                callback(new Error('密码不能低于6位数'));
            }
            else {
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
                checkPass: ''
            },
            rules: {
                pass: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                checkPass: [
                    { validator: validatePass2, trigger: 'blur' }
                ],
            }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    api.resetpasswd({
                        token:getLocalStorage('token'),
                        user_id:getLocalStorage('user_id'),
                        password:this.ruleForm.pass,
                        re_password:this.ruleForm.checkPass
                    }).then(res => {
                        if (res.code == 200){
                            this.$message.success('修改成功')
                            localStorage.clear()
                            this.$router.replace({path:'/login'})
                        }else{
                            this.$message.error('修改失败')
                        }
                    })
                } else {
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        back() {
            this.$router.back();
        }
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

</style>
