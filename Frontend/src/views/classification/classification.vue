<template>
    <div>
        <Nav></Nav>
        <div class="class_container">
            <el-tabs v-model="activeName" @tab-click="handleClick(activeName)" stretch="true">
                <el-tab-pane v-for ="(tab,index) in tabItem" :label="tab.name" :name="tab.label" :key="index">
                    <el-radio-group v-model="order" @change="orderType" class="order_type">
                        <el-radio :label="0">按时间</el-radio>
                        <el-radio :label="1">按浏览量</el-radio>
                        <el-radio :label="2">按点赞数</el-radio>
                    </el-radio-group>
                </el-tab-pane>
                <div v-for="(item,index) in data" :key="index">
                    <articleList :item="item"></articleList>
                </div>
                <div v-if="data.length ==0" class="no_class">当前分类没有信息哦~</div>
                <pagination :total="total" @getNewList="getNewList" :currentPage="this.params.page" class="pagination"></pagination>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    import Nav from '../../components/navBar/nav'
    import pagination from '../../components/pagination/pagination'
    import api from '../../../src/api/article'
    import articleList from "../../components/articleList/articleList";
    import {getLocalStorage} from "../../utils/auth";
    import {EventBus} from "../../api/busEvent";

    export default {
        name: "classification",
        data(){
          return{
              activeName: this.$route.query.id || '1001',
              data:[],
              total:0,
              order:0,
              tabItem:[
                  {label:'1001',name:'前端'},
                  {label:'1002',name:'后端'},
                  {label:'1003',name:'移动端'},
                  {label:'1004',name:'服务器'},
                  {label:'1005',name:'运营'},
                  {label:'1006',name:'产品'},
                  {label:'1007',name:'测试'},
                  {label:'1008',name:'设计'},
                  {label:'1009',name:'其他'},
              ],
              params:{type_id:this.$route.query.id || '1001',page:1,token:getLocalStorage('token'),order_type:this.order || 0}
          }
        },
        created() {
            this.querryList()
        },
        components:{
            Nav,
            pagination,
            articleList
        },
        methods:{
            querryList(){
                EventBus.$emit('resetFlag',false)
                api.getQueryArticle(this.params).then(res => {
                    this.total = res.article_count;
                    this.data = res.article;
                    console.log(res)
                })
            },
            orderType(val){
              this.params.order_type = val
              this.querryList(this.params)
            },
            handleClick(val){
                if(val != this.params.typeID){
                    this.params.page = 1
                    this.order = 0
                    this.params.order_type = 0
                    this.params.type_id = val
                    this.querryList()
                }
            },
            getNewList(val){
                this.params.page = val
                this.querryList()
            },
        }
    }
</script>

<style lang="scss" scoped>
.class_container{
    width: 960px;
    background-color: #fff;
    margin: 8px auto;
    padding: 10px;
    position: relative;
    .order_type{
        position: absolute;
        right: 15px;
        padding-bottom: 15px;
        overflow: hidden;
    }
    .no_class{
        font-size: 15px;
        text-align: center;
        color: #6c778c;
        margin: 30px 0;
    }
}
</style>
