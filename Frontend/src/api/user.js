import request from '@/utils/request'

export default {
  // 登录
  login (data) {
    return request({
      url: '/users/login',
      method: 'post',
      data
    })
  },
  register(data){
    return request({
      url:'/users/reg',
      method:'post',
      data
    })
  },
  //未登陆状态下修改密码
  resetPassword(data){
    return request({
      url:'/users/forgetpasswd',
      method:'post',
      data
    })
  },
  // 上传图片或者视频接口
  uploadPhoto(data){
    return request({
      url:'/users/uploadfiles',
      method:'post',
      data
    })
  },
  // 修改用户信息
  editUserInfo(data) {
    return request({
      url: '/users/update',
      method: 'post',
      data
    })
  },
  // 发送密码和token接口(未登陆状态下修改密码)
  changepasswd(data) {
    return request({
      url: '/users/changepasswd',
      method: 'post',
      data
    })
  },
  resetpasswd(data){
    return request({
      url:'/users/resetpasswd',
      method:'post',
      data
    })
  },
  // 登录生成验证码
  getVercode() {
    return request({
      url:'/users/getcaptcha',
      method:'get'
    })
  },
  // 搜索私信对象
  getUsers(data) {
    return request({
      url:'/users/search?q=' + data,
      method:'get'
    })
  },
  //校验token有效性
  checkToken(data) {
    return request({
        url: '/users/checktoken',
        method: 'post',
        data
     })
  },
  // 获取用户信息
  getUserInfo(data) {
    return request({
      url: '/users/info_json',
      method: 'post',
      data
    })
  },
  // 私信接口检验token
  checkMsgToken(data) {
    return request({
      url: '/chat/check',
      method: 'post',
      data
    })
  }
}
