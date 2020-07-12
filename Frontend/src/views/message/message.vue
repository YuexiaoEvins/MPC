<template>
    <div>
        <Nav style="position:sticky;"></Nav>
        <div class="content">
            <el-col :span="7">
                <div class="search_item">
                    <el-input placeholder="请输入内容" v-model="search" class="input-with-select" @input="debounce(searchUser)()">
                    </el-input>
                </div>
                <el-menu default-active="1" class="el-menu-vertical-demo" v-if="showResult">
                    <el-menu-item v-if="noUser">查无此人……</el-menu-item>
                    <el-menu-item  v-for="item in serchUsers" :key="item.user_id" @click="addList(item)" :index="item.user_id">
                        <img class="user_avatar" :src="item.user_url">
                        <span slot="title">{{ item.user_name }}</span>
                    </el-menu-item>
                </el-menu>
                <el-menu default-active="1" class="el-menu-vertical-demo" v-else>
                    <el-menu-item  v-for="item in users" :key="item.user_id" @click="chat(item)" :index="item.user_id">
                        <img class="user_avatar" :src="item.user_url">
                        <span slot="title">{{ item.user_name }}</span>
                    </el-menu-item>
                </el-menu>
            </el-col>
            <div class="chat_window" v-if="chatShow">
                <div class="chat_name">{{ current.user_name }}</div>
                <div class="chat_content" @scroll="onScroll(current.user_id)">
                    <div class="loadmore"><i class="el-icon-loading" v-if="!noMore"></i> {{ more_msg }}</div>
                    <div class="chat_message" v-for="item in current.message" :key="item">
                        <div class="other_side" v-if="!item.role">
                            <img :src="current.user_url" class="message_avatar">
                            <div class="message_content"> {{ item.content }}</div>
                            <div class="corr">
                                <em class="arrline">◆</em>
                                <span class="arrclr">◆</span>
                            </div>
                        </div>
                        <div class="my_side" v-else>
                            <div class="message_content"> {{ item.content }}</div>
                            <img :src="user.user_url" class="message_avatar">
                            <div class="corr">
                                <em class="arrline">◆</em>
                                <span class="arrclr">◆</span>
                            </div>
                        </div>
                    </div>
                    <div class="ready_message chat_message" v-for="item in current.readymsg" :key="item">
                        <div class="my_side">
                            <div class="tip">{{tip}}</div>
                            <div class="message_content"> {{ item.content }}</div>
                            <img :src="user.user_url" class="message_avatar">
                            <div class="corr">
                                <em class="arrline">◆</em>
                                <span class="arrclr">◆</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="chat_textbox">
                    <textarea v-model="mymsg" @keyup.enter="onSubmit(current.user_id)" @input="submittip=false"></textarea>
                    <el-button type="primary" @click="onSubmit(current.user_id)">发送</el-button>
                    <div v-if="submittip">
                        <div class="submit_tip">
                            <div>不能发送空白信息</div>
                        </div>
                        <div class="tip_corr">
                            <em class="tip_arrline">◆</em>
                            <span class="tip_arrclr">◆</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import myimg from "../../assets/unlogin.png"
    import Nav from '../../components/navBar/nav'
    import api from '../../api/user'
    import {getLocalStorage} from "../../utils/auth";
    import {EventBus} from "../../api/busEvent";

    export default {
        name: "message",
        data() {
            return {
                socket: "",
                chatShow: false,
                myimg: myimg,
                mymsg: '', // 输入框
                user : { // 登录用户
                    id: getLocalStorage('user_id'),
                    user_name: getLocalStorage('user_name'),
                    user_url: getLocalStorage('user_url'),
                    token: getLocalStorage('token')
                },
                users: [], // 对话用户列表
                serchUsers: [], // 搜索用户列表
                current:{ // 当前对话用户
                    user_id: '0',
                    user_name:'',
                    user_url:'',
                    message: [],// 0代表对方，1代表自己
                    readymsg: [], // 未送达的消息
                },
                tip:'发送中…',
                more_msg: '查看更多',
                noMore: false,
                search:'', // 搜索关键字
                showResult: false,
                noUser: false,
                submittip: false,
                path:''
            };
        },
        methods: {
            searchUser() {
                if(this.search == '') {this.showResult = false; return}
                else {
                    this.showResult = true;
                    api.getUsers(this.search).then(res => {
                        console.log(res)
                        this.noUser = false
                        this.serchUsers = res.user
                        if(res.user.length == 0) {this.noUser = true}
                        // console.log(res)
                    })
                }
            },
            debounce(handle) { //防抖
                let timer;
                return function() {
                    var _this = this, // setTimeout形成闭包
                        _arg = arguments; // 事件对象
                    clearTimeout(timer);
                    timer = setTimeout(() => {
                        handle.apply(_this, _arg);
                    }, 800)
                }
            },
            addList(cur) {
                this.users.unshift(cur);
                this.showResult = false;
                this.noUser = false
                this.search = ''
                this.chat(cur)
            },
            chat(cur) { // 建立对话
                // console.log(cur)
                api.checkMsgToken({
                    token: this.user.token
                }).then(res => {
                    if(res.code == 200 ){
                        this.chatShow = true;
                        this.current = cur;
                        this.current.message = [];
                        this.current.readymsg = [];
                        this.more_msg = '查看更多';
                        this.noMore = false;
                        this.path = 'ws://192.168.91.5:8008/ws/chat/' + this.user.id + '-' + cur.user_id + '/';
                        if (typeof (WebSocket) === "undefined") {
                            alert("您的浏览器不支持socket")
                        } else {
                            this.socket = new WebSocket(this.path) // 实例化socket
                            this.socket.onopen = this.open // 监听socket连接
                            this.socket.onerror = this.error // 监听socket错误信息
                            this.socket.onmessage = this.getMessage // 监听socket信息
                        }
                    }
                })
            },

            open: function () {
                console.log("socket连接成功")
            },
            error: function () {
                console.log("连接错误")
                this.reconnect()
            },
            close: function () {
                console.log("socket已经关闭")
            },
            reconnect() {
                setTimeout(function () {     //没连接上会一直重连，设置延迟避免请求过多
                    this.socket = new WebSocket(this.path);
                    this.socket.onclose = function () {
                        this.reconnect()
                    };
                    this.socket.onerror = function () {
                        this.reconnect()
                    };
                    }, 2000);
            },
            getMessage: function (msg) { // 接收信息
                let data = JSON.parse(msg.data);
                console.log(data)
                if(data[0].send_type) this.addmessage(data);
                else this.addrecord(data);

            },

            addrecord(record) { // 添加聊天记录
                console.log('addrecord')
                if(record[0].is_end) {
                    this.noMore = true;
                    this.more_msg = '没有更多了'
                } else {
                    if(record[0].is_first_hist) {
                        if(record.length < 10) this.noMore = true;
                        this.current.message = record.concat(this.current.message);
                        this.$forceUpdate();
                        this.$nextTick(() => {
                            this.scrollToBottom();
                        });
                    } else {
                        let container = document.getElementsByClassName('chat_content');
                        let height = container[0].scrollHeight;
                        this.current.message = record.concat(this.current.message);
                        this.$forceUpdate();
                        this.$nextTick(() => {
                            container[0].scrollTop = container[0].scrollHeight - height;
                        });
                    }
                }
            },
            addmessage(msg) { // 添加新信息
                console.log('addmessage')
                for(let i in msg) {
                    if(msg[i].role && this.current.readymsg.length){ 
                        this.current.readymsg.shift();
                    }
                    this.current.message.push(msg[i]);
                    if(msg[i].role) {
                        EventBus.$emit('sentMqtt',`${this.current.user_id + "*&^*&^" + this.user.user_name + "*&^*&^" + 'message'}`,this.current.user_id)
                        console.log('ffff')
                    }
                    this.$forceUpdate(); // 强制渲染
                }
                this.scrollToBottom();
            },
            onSubmit(to_id) { // 发送新消息
                let trim = this.mymsg.replace( /^\s*/, '');
                if(trim === '') { this.submittip = true; return }
                let curmsg = {
                    content: this.mymsg,
                    from_id: this.user.id,
                    to_id: to_id,
                    send_type: 1
                }
                this.socket.send(JSON.stringify(curmsg));
                this.current.readymsg.push(curmsg)
                console.log(this.current.readymsg)
                this.mymsg = '';
                this.scrollToBottom();
            },
            onScroll(to_id) { // 上拉加载
                let container = document.getElementsByClassName('chat_content');
                let scrollTop = container[0].scrollTop;
                if(scrollTop == 0 && !this.noMore) {
                    let loadmore = {
                        from_id: this.user.id,
                        to_id: to_id,
                        sequence_id: this.current.message[0].sequence_id,
                        send_type: 0
                    }
                    this.socket.send(JSON.stringify(loadmore));
                }
            },
            scrollToBottom() {   // 滑动条在最下方
                let container = document.getElementsByClassName('chat_content');
                container[0].scrollTop = container[0].scrollHeight;
            },
        },
        created(){
            if(this.$route.query.id){
                api.getUserInfo({
                    user_id: this.$route.query.id,
                    token: getLocalStorage('token')
                }).then(res => {
                    // onsole.log(res)
                    this.users = [{
                        user_id: res.user.user_id,
                        user_name: res.user.user_name,
                        user_url: res.user.user_url,
                    }]
                })
            }
        },
        destroyed() {
            // 销毁监听
            this.socket.onclose = this.close
        },
        components: {
            Nav
        }
    }
</script>
<style lang="scss" scoped>
    .content{
        width: 1000px;
        height: 700px;
        margin: 10px auto;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(26,26,26,.1);
    }
    .el-col {
        border-right: solid 1px #e6e6e6;
    }
    .user_avatar{
        width: 35px;
        height: 35px;
        margin-right: 5px;
    }
    .el-menu {
        height: 619px;
        border: 0px;
        overflow-y: auto;
    }
    .el-menu-item.is-active {
        background-color: #f4f7ff;
    }
    .el-menu-item::after {
        content: "";
        position: absolute;
        right: 20px;
        left: 20px;
        bottom: 0;
        height: 1px;
        background-color: #f7f8fa;
    }
    .search_item {
        padding: 20px 20px !important;
        border-bottom: solid 1px #e6e6e6;
    }
    .chat_window {
        padding-left: 30%;
        padding-right: 2%;
        .chat_name {
            font-size: 20px;
            height: 50px;
            text-align: center;
            line-height: 50px;
            border-bottom: 1px solid #e6e6e6;
        }
        .chat_content {
            height: 420px;
            overflow-y: auto;
        }
        .loadmore {
            color:#d6d6d6;
            text-align: center;
        }
        .chat_textbox {
            height: 230px;
            border-top: 1px solid #e6e6e6;
        }
        .chat_message {
            margin: 20px 0px;
            .message_avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                // border: 1px solid #8DAFFC;
            }
            .message_content {
                background-color: #f6f6f6;
                // width: 500px;
                // height: 200px;
                display: inline-block;
                vertical-align: top;
                border-radius: 10px;
                font-size: 14px;
                padding: 10px;
            }
            .corr {
                width: 13px;
                height: 14px;
                overflow: hidden;
            }
            .arrline {
                color: #f6f6f6;
                display: block;
                font-family: "SimSun";
                font-size: 15px;
                font-style: normal;
                font-weight: normal;
                height: 10px;
                line-height: normal;
                text-align: left;
            }
            .arrclr {
                color: #f6f6f6;
                display: block;
                font-family: "SimSun";
                font-size: 15px;
                font-style: normal;
                font-weight: normal;
                height: 10px;
                line-height: normal;
            }
            .other_side {
                position: relative;
                .message_content {
                    margin-left: 10px;
                }
                .corr {
                    position: absolute;
                    left: 42px;
                    top: 10px;
                }
                .arrclr {
                    margin: -10px 0 0 1px;
                }
            }
            .my_side {
                position: relative;
                margin-right: 20px;
                text-align: right;
                .message_content {
                    margin-right: 10px;
                }
                .corr {
                    position: absolute;
                    right: 44px;
                    top: 10px;
                }
                .arrclr {
                    margin: 0 0 0 10px;
                }
                .tip {
                    display: inline-block;
                    vertical-align: bottom;
                    color: #d6d6d6;
                }
            }
        }
        .chat_textbox {
            position: relative;
            padding-top: 10px;
            textarea {
                height: 150px;
                width: 680px;
                display: block;
                padding: 5px 6px 6px;
                line-height: 19px;
                resize: none;
                overflow: auto;
                outline: none;
                border: none;
                font-size: 15px;
                font-family: inherit;
            }
            .el-button {
                float: right;
            }
            .submit_tip {
                position: absolute;
                right:0px;
                top: 110px;
                background: #fff;
                width: 115px;
                border-radius: 4px;
                border: 1px solid #ebeef5;
                padding: 12px;
                color: #606266;
                line-height: 1.4;
                text-align: justify;
                font-size: 14px;
                box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
                word-break: break-all;
            }
            .tip_corr {
                position: absolute;
                top: 145px;
                right: 0px;
                width: 30px;
                height: 14px;
                overflow: hidden;
            }
            .tip_arrline {
                color: #fff;
                display: block;
                font-family: "SimSun";
                font-size: 15px;
                font-style: normal;
                font-weight: normal;
                height: 10px;
                line-height: normal;
                text-align: left;
            }
            .tip_arrclr {
                color: #fff;
                display: block;
                font-family: "SimSun";
                font-size: 15px;
                font-style: normal;
                font-weight: normal;
                height: 10px;
                line-height: normal;
                border: 1px solid #ebeef5;
            }
        }
    }
</style>
