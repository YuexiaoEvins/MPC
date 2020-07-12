<template>
    <div class="pagination">
        <el-pagination
                background
                layout="prev, pager, next"
                page-size="10"
                :total="total"
                @current-change="currentChange"
                :current-page="currentPage"
            >
        </el-pagination>
    </div>
</template>

<script>
    export default {
        name: "pagination",
        props: {
            currentPage: {
                type:Number,
                default:1
            },
            total:{
                type:Number,
                default: 1
            }
        },
        methods:{
            currentChange(val){
                this.$emit('getNewList',val)
            }
        }
    }
</script>

<style scoped>
.pagination{
    text-align: center;
    margin-bottom: 15px;
}
</style>
