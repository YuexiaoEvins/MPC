<template>
    <div class="not_found_container">
        <div class="text_tips">
           <div>找不到当前页面辣~</div>
            <a href="" class="backBtn">点击返回首页</a>
        </div>
        <div class="img_container">
            <img class="img_cloud_left left" src="../../assets/404_cloud.png" alt="">
            <img class="img_cloud_center center" src="../../assets/404_cloud.png" alt="">
            <img class="img_cloud_right right" src="../../assets/404_cloud.png" alt="">
            <img class="img_404" src="../../assets/404.png" alt="">
        </div>

    </div>
</template>

<script>
    export default {
        name: "404page"
    }
</script>

<style lang="scss" scoped>
 .not_found_container {
     position: absolute;
     top: 40%;
     left: 50%;
     transform: translate(-50%, -50%);
     display: inline-block;
     .text_tips{
         text-align: center;
         font-size: 32px;
         font-weight:bold;
         color:#8DAFFC;
         animation-name:slideUp;
         animation-timing-function: linear;
         animation-fill-mode: forwards;
         animation-duration: 0.5s;
         position: relative;
         .backBtn{
             background-color: #8DAFFC;
             color: #fff;
             font-size: 16px;
             font-weight: lighter;
             padding: 8px;
             border-radius: 3px;
         }
         @keyframes slideUp {
            0%{
              top:50px;
              opacity: 0;
           }
            50%{
                 top:25px;
                 opacity: 0.5;
             }
            100%{
                 top:0;
                 opacity: 1;
             }

         }
     }
     .img_container{
         margin-top: 15px;
         .img_cloud_left{
            width: 100px;
            position: absolute;
            left:10%;
            top:10%;
            &.left{
                animation-name: cloudLeft;
                animation-duration: 1.5s;
                animation-timing-function: ease;
                animation-fill-mode: forwards;
            }
             @keyframes cloudLeft {
                 0%{
                     top:15%;
                     left:10%;
                     opacity:0;
                 }
                 50%{
                     top:20%;
                     left: 5%;
                     opacity: 1;
                 }
                 100%{
                     top:25%;
                     left:0%;
                     opacity: 0;
                 }
             }
         }
         .img_cloud_center{
             width: 60px;
             position: absolute;
             left:30%;
             top:40%;
             &.center{
                 animation-name: cloudCenter;
                 animation-duration: 1.5s;
                 animation-timing-function: ease;
                 animation-fill-mode: forwards;
             }
             @keyframes cloudCenter {
                 0% {
                    top:45%;
                    left:30%;
                    opacity: 0;
                 }
                 50%{
                    top:55%;
                    left:25%;
                    opacity: 1;
                 }
                 100% {
                     top:65%;
                     left:20%;
                     opacity: 0;
                 }
             }
         }
         .img_cloud_right{
             width: 80px;
             position: absolute;
             left:60%;
             top:30%;
             &.right{
                 animation-name: cloudRight;
                 animation-duration: 1.5s;
                 animation-timing-function: ease;
                 animation-fill-mode: forwards;
             }
             @keyframes cloudRight {
                  0% {
                      top:40%;
                      left:50%;
                      opacity: 0;
                  }
                  50%{
                      top:55%;
                      left:40%;
                      opacity: 1;
                  }
                  100% {
                      top:70%;
                      left:30%;
                      opacity: 0;
                  }
              }
         }
    }
     .img_404 {
         height: 320px;
     }
 }
</style>
