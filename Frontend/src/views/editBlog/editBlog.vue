<template>
    <div>
        <Nav></Nav>
        <div class="main" id="main">
            <textarea class="title" v-model="title" placeholder="请输入标题（不超过30个字）" maxlength="30"></textarea>
            <div class="tag_radio">
                请选择一个分类：
                <el-radio border v-for="item in tags" :key="item" :label="item.id" v-model="radio">{{ item.name }}</el-radio>
            </div>
            <Editor id="tinymce" v-model="tinymceHtml" :init="editorInit" placeholder="请输入正文"></Editor>
            <el-button type="primary" icon="el-icon-s-promotion" @click="send(1)" :disabled="isNull">发布</el-button>
            <el-button class="draft_btn" icon="el-icon-takeaway-box" @click="draft(0)" plain>存入草稿箱</el-button>
            <el-button class="preview_btn" icon="el-icon-data-board" @click="open" plain>预览页面</el-button>
            <el-drawer :visible.sync="drawer" :direction="direction" :with-header="false" size="60%">
                <div class="showtitle">{{title}}</div>
                <div class="showcontent" v-html="tinymceHtml"></div>
            </el-drawer>
        </div>
    </div>
</template>

<script>
    var articleId = ''
    import Nav from '../../components/navBar/nav'
    import 'tinymce/skins/ui/oxide/skin.min.css'; //富文本样式
    import tinymce from 'tinymce/tinymce'; //配置富文本
    import 'tinymce/themes/silver/theme.min.js' //引入富文本的主要脚本
    import Editor from '@tinymce/tinymce-vue'; //引用富文本组件
    import 'tinymce/plugins/image' // 上传图片插件
    import 'tinymce/plugins/media' // 上传视频插件
    import 'tinymce/plugins/link'
    import 'tinymce/plugins/code'
    import 'tinymce/plugins/table'
    import 'tinymce/plugins/lists'
    import 'tinymce/plugins/contextmenu'
    import 'tinymce/plugins/wordcount'
    import 'tinymce/plugins/media'
    // import api from '../../api/user'
    import articleApi from '../../api/article'
    import Message from "element-ui/packages/message/src/main";
    import {getLocalStorage} from "../../utils/auth";

    export default {
        props: {
            value: {
                type: String,
                default:''
            }
        },
        name: "editBlog",
        data () {
            return {
                drawer: false,
                direction: 'rtl',
                tinymceHtml: this.value,
                title:'',
                isNull: true,
                radio: 1009,
                text:'',
                article_id:'',
                ifSend:'存入草稿箱',
                sentType:0,
                tags: [
                    { id: 1001, name: '前端' },
                    { id: 1002, name: '后端' },
                    { id: 1003, name: '移动端' },
                    { id: 1004, name: '服务器端' },
                    { id: 1005, name: '运营' },
                    { id: 1006, name: '产品' },
                    { id: 1007, name: '测试' },
                    { id: 1008, name: '设计' },
                    { id: 1009, name: '其他' },
                ],
                editorInit: {
                    language_url: '/tinymce/zh_CN.js',
                    language: 'zh_CN',
                    skin_url: '/tinymce/skins/lightgray',
                    height: 600,
                    plugins: 'link lists image code table colorpicker textcolor wordcount contextmenu media ',
                    toolbar:
                        'bold italic | fontsizeselect | bullist numlist | undo redo | link unlink image media code | removeformat',
                    branding: false,
                    menubar: false,
                    resize:false,
                    content_style: `
                    * { padding:0; margin:0; }
                    img {max-width:50%; height:auto;margin:auto;display:block;}
                    `,
                    paste_data_images: true, // 粘贴的同时能把内容里的图片自动上传
                    image_dimensions: false, // 用户修改尺寸
                    maxSize: 2100000, // 文件大小2M
                    // media_live_embeds: true, // 用户可看到编辑区内嵌入视频的实时预览，而不是占位图
                    // media_alt_source: false, // 显示隐藏资源备用地址输入框
                    media_dimensions: false, // 显示隐藏宽高尺寸输入框
                    // media_poster: true,
                    // 此处为图片上传处理函数
                    images_upload_handler: (blobInfo, success, failure) => {
                        if (blobInfo.blob().size > this.maxSize) {
                            failure('图片大小不能超过2M')
                        }
                        let formdata;
                        formdata = new FormData();
                        formdata.append('photo',blobInfo.blob())
                        formdata.append('token',getLocalStorage('token'))
                        formdata.append('article_id',articleId)
                        articleApi.uploadPhoto(formdata).then(res => {
                            console.log(res);
                            success(res.photo_name)
                        })
                    },
                    file_picker_types: 'media',
                    file_picker_callback: function(callback, value, meta) {
                        if(meta.filetype == 'media') {
                            // 给input加accept属性来限制上传的文件类型
                            let input = document.createElement('input');
                            input.setAttribute('type', 'file');
                            input.click();
                            let file, formData;
                            input.onchange = function() {
                                file = this.files[0];
                                var fileSize = (file.size / 1024/1024).toFixed(0)
                                var fileType = file.name.substring(file.name.lastIndexOf(".")+1)
                                // console.log(fileType)
                                if(fileType != 'mp4'){
                                    Message.error('上传视频格式只能为MP4~')
                                    // alert('上传视频格式只能为MP4~')
                                    return false
                                }else if(fileSize > 30) {
                                    Message.error('上传视频不能超过30M~')
                                    // alert('上传视频不能超过30M~')
                                    return false
                                }else {
                                    //假设接口接收参数为file,值为选中的文件
                                    formData = new FormData();
                                    formData.append('photo', file);
                                    formData.append('token', getLocalStorage('token'));
                                    formData.append('article_id', articleId);
                                    articleApi.uploadPhoto(formData).then(res => {
                                        console.log(res);callback(res.photo_name, {poster: res.shot_name})})
                               }
                            }
                            // let poster = document.getElementsByClassName()
                        }
                    },
                }
            }
        },
        methods: {
            open() {
                this.drawer = true;
                console.log(this.drawer)
            },
            saveArticle(val){
                // articleApi.saveArticle({
                //     token:getLocalStorage('token'),
                //     article_id:articleId,
                //     title:this.title,
                //     user_id:getLocalStorage('user_id'),
                //     content:this.tinymceHtml,
                //     type_id: this.radio,
                //     flag:val
                // }).then(() => {
                //     if(val == 1){
                //         Message.success('发布成功')
                //     }else {
                //         Message.success('存入草稿成功')
                //     }

            },
                // ).catch(
                //     Message.error(err => '发送失败')
                // )

            send(val) {
                this.ifSend = '发布'
                this.sentType = val
                this.$router.push({path:'/hotPoint'})
            },
            draft(val) {
                this.ifSend = '存入草稿箱'
                this.sentType = val
                this.$router.push({path:'/hotPoint'})
            },
    },

        watch: {
            value (newValue) {
                console.log(newValue);
                this.tinymceHtml = newValue;
            },
            tinymceHtml (newValue) {
                if (newValue.trim() == '' || this.title.trim() == '') this.isNull = true;
                else this.isNull = false;
                this.$emit('input', newValue)
            },
            title (newValue) {
                if (newValue.trim() == '' || this.title.trim() == '') this.isNull = true;
                else this.isNull = false;
                this.title = newValue;
            }
        },
        created(){
            if (this.$route.query.ifEdit == true){
                articleApi.editArticle({token:getLocalStorage('token'),article_id:this.$route.query.articleId})
                    .then(res => {
                        console.log(res)
                        let data = res.comment
                        articleId = data[0].article_id
                        this.title = data[0].title
                        this.tinymceHtml = data[0].content
                        this.radio = data[0].type_id
                    })
            }else{
                articleApi.createArticleId({token:getLocalStorage('token'),type_id:'1009'})
                    .then(res => {
                        articleId = res.article_id
                        console.log(res)
                    })
            }
        },
        mounted() {
            tinymce.init({})
        },
        components: {Editor,Nav},
        beforeRouteLeave (to, from , next) {
            this.$confirm(`是否${this.ifSend}`, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                articleApi.saveArticle({
                    token:getLocalStorage('token'),
                    article_id:articleId,
                    title:this.title,
                    user_id:getLocalStorage('user_id'),
                    content:this.tinymceHtml,
                    type_id: this.radio,
                    flag:this.sentType
                }).then(() => {
                    if(this.ifSend == '发布') Message.success(`${this.ifSend}成功，积分+5`)
                    else Message.success(`${this.ifSend}成功`)
                    next()
                }
                ).catch(
                    Message.error(err => `${this.ifSend}失败`)
                )
            }).catch((err) => {
               next()
                })
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
        padding-bottom: 70px;
    }
    .title {
        height: 44px;
        display: block;
        width: 100%;
        border: 0;
        font-family: 'Arial';
        font-size: 30px;
        font-weight: 600;
        line-height: 1.4;
        outline: none;
        -webkit-box-shadow: none;
        box-shadow: none;
        resize: none;
    }
    .tag_radio {
        margin: 20px 0px;
        font-size: 15px;
        /deep/ .el-radio__inner {
            border: 0;
            width: 0;
            height: 0;
        }
        /deep/ .el-radio__input {
            height: 0;
            line-height: unset;
        }
        .el-radio {
            padding: 0px 15px;
            height: 35px;
            line-height: 35px;
            margin-right: 0px;
        }
        /deep/ .el-radio__label {
            padding: 0;
            font-size: 15px;
        }
        .el-radio.is-bordered.is-checked {
            background: #f4f7ff;
        }
    }
    .el-button {
        float: right;
        margin-top: 10px;
    }
    .preview_btn:hover {
        color: #8DAFFC;
        border-color: #8DAFFC;
        background: #fff;
    }
    .preview_btn:focus {
        color: #8DAFFC;
        border-color: #8DAFFC;
        background: #fff;
    }
    .draft_btn {
        margin-right: 10px;
        color: #8DAFFC;
        border-color: #8DAFFC;
    }
    .draft_btn:hover {
        color: #8DAFFC !important;
        border-color: #8DAFFC !important;
        background-color: #f4f7ff !important;
    }
    .showtitle {
        margin: 20px 0 0 20px;
        font-family: 'Arial';
        font-size: 32px;
        font-weight: 600;
    }
    .showcontent {
        margin: 20px;
        font-size: 14px;
    }
    .showcontent /deep/ img {
        max-width: 90%;
        height: auto;
        display: block;
    }
    .showcontent /deep/ video {
        width:90% !important;
        height:auto;
        margin:auto;
        display:block;
    }
    .main /deep/ .el-drawer{
        overflow: auto;
    }
</style>
