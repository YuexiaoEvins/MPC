import Vue from 'vue'
import Router from 'vue-router'
import {getLocalStorage} from "../utils/auth";
import api from '../api/user'
const whiteList = ['/login','/register','/resetPassword','/sentPassword']
import Message from "element-ui/packages/message/src/main";
Vue.use(Router)

 const router = new Router({
    routes: [
        {
            path: '/',
            name: 'index',
            redirect:'/hotPoint',
            component:  () => import('../views/index'),
            children:[
                {
                    path:'follow',
                    name:'follow',
                    component:()=> import('../views/follow/follow')
                },
                {
                    path:'hotPoint',
                    name:'hotPoint',
                    component:()=> import('../views/hotPoint/hotPoint')
                }
            ]
        },
        {
            path:'/login',
            name:'login',
            component: ()=>import('../views/login/login')
        },
        {
            path:'/register',
            name:'register',
            meta:{keepAlive:false},
            component: ()=>import('../views/register/register')
        },
        {
            path:'/userinfo',
            name:'userinfo',
            component: ()=>import('../views/userinfo/userinfo'),
        },
        {
            path:'/editinfo',
            name:'editinfo',
            component: ()=>import('../views/userinfo/editinfo')
        },
        {
            path:'/editpsw',
            name:'editpsw',
            component: ()=>import('../views/userinfo/editpsw')
        },
        {
            path:'/message',
            name:'message',
            component: ()=>import('../views/message/message')
        },
        {
            path:'/editBlog',
            name:'editBlog',
            component: () => import('../views/editBlog/editBlog')
        },
        {
            path:'/articleDetail',
            name:'articleDetail',
            component:() => import('../views/articleDetail/articleDetail')
        },
        {
            path:'/classification',
            name:'classification',
            component:()=> import('../views/classification/classification')
        },
        {
            path:'/draft',
            name:'draft',
            component:()=> import('../views/editBlog/draft')
        },
        {
            path:'/resetPassword',
            name:'resetPassword',
            component:()=>import('../views/resetPassword/resetPassword')
        },
        {
            path:'/sentPassword',
            name:'sentPassword',
            component:()=>import('../views/sentPassword/sentPassword')
        },
        {
            path:'/searchResult',
            name:'searchResult',
            component:()=>import('../views/searchResult/searchResult')
        },
        {
            path:'*',
            component:()=> import('../views/404page/404page')
        }
    ]
})


router.beforeEach((to,from,next)=>{
    if (getLocalStorage('token')){
            if(to.name == 'login' || to.name == 'register' || to.name == 'resetPassword' || to.name == 'resetPassword'){
                next()
            }else{
                 api.checkToken({token:getLocalStorage('token')}).then(res =>{
                     console.log(res)
                    if(res.code === 401){
                            next('/login')
                        }else{
                            next()
                        }
                }).catch(err => {
                     Message.info('请重新登陆')
                     next('/login')
                })
            }
    }else {
        if(whiteList.indexOf(to.path)!== -1){
            next()
         }else{
            next('/login')
        }
    }
})

export default router

