<template>
    <div class="article_container">
        <el-radio-group v-model="order_type" @change="orderType" class="order_type">
            <el-radio :label="0">按时间</el-radio>
            <el-radio :label="1">按浏览量</el-radio>
            <el-radio :label="2">按点赞数</el-radio>
        </el-radio-group>
        <div v-for="(item,index) in result" :key="index">
            <articleList :item="item"></articleList>
        </div>
        <pagination :total="total" @getNewList="getNewList" v-if="total"></pagination>
    </div>
</template>

<script>
    import api from '../../api/article';
    import articleList from "../../components/articleList/articleList";
    import pagination from '../../components/pagination/pagination'
    import {getLocalStorage} from "../../utils/auth";
    import {EventBus} from "../../api/busEvent";

    export default {
        name: "hotPoint",
        data(){
            return{
             order_type:0,
             result:[],
             total:0,
             page:1
            }
        },
        created(){
            this.getIndexInfo()
        },
        methods:{
            getIndexInfo(){
                EventBus.$emit('resetFlag',false)
                api.getIndexInfo({
                        page:this.page,
                        token:getLocalStorage('token'),
                        order_type:this.order_type,
                        user_id:getLocalStorage('user_id'),
                    }
                ).then(res => {
                    this.result = res.article
                    this.total = res.article_count
                    console.log(res)
                })
            },
            goArticle(){
                console.log('goArticle')
            },
            getNewList(val){
                console.log(val)
                this.page = val
                this.getIndexInfo()
            },
            orderType(val){
                this.order_type = val
                EventBus.$emit('resetFlag',false)
                this.getIndexInfo()
            }
        },
        components:{
            articleList,
            pagination
        },

    }
</script>

<style lang="scss" scoped>
    .article_container{
        position: relative;
        .order_type{
            position: absolute;
            right: 15px;
        }
     }
</style>
