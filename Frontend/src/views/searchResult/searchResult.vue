<template>
    <div>
        <Nav style="position: sticky"></Nav>
        <div class="container">
            <div v-if="List.length == 0">没有搜索到您当前输入的内容哦~</div>
            <div v-for="(item,index) in List" :key="index">
                <articleList :item="item"></articleList>
            </div>
            <pagination :total="total" @getNewList="getNewList" ></pagination>
        </div>
    </div>
</template>

<script>
    import Nav from "../../components/navBar/nav";
    import articleList from "../../components/articleList/articleList";
    import pagination from '../../components/pagination/pagination';
    import api from '../../api/article';
    import {getLocalStorage} from "../../utils/auth";

    export default {
        name: "searchResult",
        data(){
            return{
                List:[],
                total:0,
                page:1
            }
        },
        components:{
            Nav,
            articleList,
            pagination
        },
        created() {
           this.search()
        },
        methods:{
            search(){
                api.searchArticle(this.$route.query.q,this.page,getLocalStorage("user_id")).then(res => {
                    this.List = res.article
                    this.total = res.article_count
                })
            },
            getNewList(val){
                this.page = val
                this.search()
            }
        }

    }
</script>

<style lang="scss" scoped>
.container{
    position: relative;
    margin: 15px auto;
    width: 960px;
    min-height: 980px;
    background-color: #fff;
    padding: 20px 10px;
}
</style>
