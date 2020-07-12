import { getLocalStorage, setLocalStorage, removeToken } from '@/utils/auth'
import api from '@/api/user'

const user = {
  state: {
    token: getLocalStorage(),
    name: '',
    avatar: '',
    roles: [],
    gender:'',
    id:'',
    account:'',
    phone:''
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ID: (state, id) => {
      state.id = id
    },
    SET_GENDER: (state,gender) => {
      state.gender = gender
    },
    SET_ACCOUNT: (state,account) => {
      state.account = account
    },
    SET_PHONE: (state,phone) => {
      state.phone = phone
    },
  },

  actions: {
    // 登录
    login ({ commit }, userInfo) {
      const { user_account, password } = userInfo
      return new Promise((resolve, reject) => {
        api.login({user_account:user_account,password:password}).then(res => {
          if(res.code == 200){
            const data = res
            setLocalStorage('token',res.token)
            setLocalStorage('user_name', res.user_name)
            setLocalStorage('user_url', res.user_url)
            setLocalStorage('user_gender', res.user_gender)
            setLocalStorage('user_phone', res.user_phone)
            setLocalStorage('user_account', res.user_account)
            setLocalStorage('user_id',res.user_id)
            setLocalStorage('email',res.email)
            setLocalStorage('credit',res.user_credit)
            console.log(data)
            resolve(data)
          }
        }).catch(err => {
          reject(err)
        })
      })
    },

    // 获取用户信息
    GetUserInfo ({ commit }) {
      return new Promise((resolve, reject) => {
        api.getUserInfo().then(res => {
          // console.log(res)
          if (res.code === 200) {
            // commit('SET_NAME', res.user_name)
            // commit('SET_AVATAR', res.user_url)
            // commit('SET_GENDER', res.user_gender)
            // commit('SET_PHONE', res.user_phone)
            // commit('SET_ACCOUNT', res.user_account)
            // commit('SET_ID',res.user_id)
          }
          resolve(res)
        }).catch(error => {
          reject(error)
        })
      })
    },
    //
    // // 登出
    // LogOut ({ commit, state }) {
    //   return new Promise((resolve, reject) => {
    //     logout(state.token).then(() => {
    //       commit('SET_TOKEN', '')
    //       commit('SET_ROLES', [])
    //       removeToken()
    //       resolve()
    //     }).catch(error => {
    //       reject(error)
    //     })
    //   })
    // },

    // 前端 登出
    FedLogOut ({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user
