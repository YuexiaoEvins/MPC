// 一些全局的config配置
const modeUrlObj = {
  // 生产环境
  'production': {
    baseURL: 'http://192.168.195.9:8888/zhifou',
    authBaseURL: ''
  },
  // 开发环境
  'development': {
    baseURL: '/api',
    authBaseURL: ''
  },
  // 测试环境
  'test': {
    baseURL: 'http://192.168.195.9:8888/zhifou',
    authBaseURL: ''
  }
}
export default modeUrlObj[process.env.NODE_ENV]
