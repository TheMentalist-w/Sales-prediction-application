import Vue from 'vue'
import VueRouter from 'vue-router'
import Products from '../Products/Products.vue'
import Login from '../Auth/Login'
import Accounts from "../Accounts/Accounts"

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/accounts',
    name: 'Accounts',
    component: Accounts
  },
  {
    path: '/',
    name: 'Products',
    component: Products
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
