<template>
  <div id="app">
      <router-view></router-view>
  </div>
</template>
<script>
    import Paho from 'paho-mqtt'
    import {getLocalStorage} from "./utils/auth";
    import {EventBus} from "./api/busEvent";

    export default {
  name: 'App',
    data(){
      return{
          reconnectTimeout: 200,
          mqtt: {},
          msg:"",
          userId:getLocalStorage('user_id')
      }
    },
  components: {
  },
    created() {
        this.MQTTconnect()
    },
    methods:{
        sentMqtt(val,id){
            this.mqtt.publish(`like/${id}`,val,1,true);
        },
        MQTTconnect() {
            this.mqtt = new Paho.Client(  //实例化一个对象
                '192.168.91.5',
                9001,
                "mqttjs" + this.userId //防止多个浏览器打开，导致的问题，保证唯一性
            );
            var options = {
                timeout: 50000,
                useSSL: false,
                cleanSession: false,
                userName :'zhifou',
                password :'123456',
                keepAliveInterval:100000,
                onSuccess: this.onconnect,
                onFailure: function() {
                    //连接失败定时重连
                    setTimeout(this.MQTTconnect, this.reconnectTimeout);
                }
            };
            this.mqtt.onConnectionLost = this.onConnectionLost;
            this.mqtt.onMessageArrived = this.onMessageArrived;
            this.mqtt.connect(options);
        },
        getuuid() {
            var uid = [];
            var hexDigits = "0123456789abcdefghijklmnopqrst";
            for (var i = 0; i < 32; i++) {
                uid[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
            }
            uid[6] = "4";
            uid[15] = hexDigits.substr((uid[15] & 0x3) | 0x8, 1);
            var uuid = uid.join("");
            return uuid;
        },
        //连接
        onconnect() {
            this.mqtt.subscribe(`like/${this.userId}`,{qos:2})
        },
        //连接丢失
        onConnectionLost(response) {
            console.log(response)
        },
        //接收到消息，处理
        onMessageArrived(message) {
            console.log(message)
            var msg = message.payloadString;
            let arr = msg.split('*&^*&^')
            console.log(arr)
            if(arr[2] == 'message'){
                console.log('fffffmessage')
                let _this = this;
                this.$notify({
                    title: '提示',
                    message: `${arr[1]}给您发私信，点击查看`,
                    type:"success",
                    duration:2000,
                    onClick() {
                        let routeUrl = _this.$router.resolve({
                            path:'/message',
                            query:{id:arr[0]}
                        })
                        window.open(routeUrl.href,"_blank")
                    }
                });
            }else if (arr[2] == 'like'){
                this.$notify({
                    title: '提示',
                    message: `${arr[1]}点赞了您的文章:${arr[0]}`,
                    type:"success",
                    duration:1500
                });
            }else{
                this.$notify({
                    title: '提示',
                    message: `${arr[1]}收藏了您的文章:${arr[0]}`,
                    type:"success",
                    duration:1500
                });
            }
            //判断主题，调用方法，这里可以订阅多个主题，在此处判断，接受不同的主题，调用不同的方法！
        },
    },
        mounted() {
          EventBus.$on('sentMqtt',(val,id)=> {
              this.sentMqtt(val,id)
          })
        }
    }
</script>
<style lang="scss">
  @import "assets/css/reset";
  body{
    background-color: #f6f6f6;
  }
</style>
