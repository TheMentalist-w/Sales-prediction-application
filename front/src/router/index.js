import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../Auth/Login')
  },
  {
    path: '/accounts',
    name: 'Accounts',
    component: () => import('../Accounts/Accounts')
  },
  {
    path: '/product/:id',
    name: 'ProductShow',
    component: () => import('../Products/Show')
  },
  {
    path: '/',
    name: 'Products',
    component: () => import('../Products/Index')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
