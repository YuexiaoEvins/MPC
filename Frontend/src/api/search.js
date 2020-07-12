import request from '@/utils/request'

export default {
    deleteAllHis(data) {
        return request({
            url:'/article/delAllHistorySearch',
            method:'post',
            data
        })
    },
    deleteOneHis(data){
        return request({
            url:'/article/delHistorySearch',
            method: 'post',
            data
        })

    }
}
