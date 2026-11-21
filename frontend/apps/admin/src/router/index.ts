import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: () => import('../views/Dashboard.vue') },
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/shops', name: 'shops', component: () => import('../views/Shops.vue') },
    { path: '/products', name: 'products', component: () => import('../views/Products.vue') },
    { path: '/users', name: 'users', component: () => import('../views/Users.vue') },
    { path: '/merchants', name: 'merchants', component: () => import('../views/Merchants.vue') },
  ],
})

export default router
