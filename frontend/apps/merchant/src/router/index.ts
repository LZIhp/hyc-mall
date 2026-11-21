import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: () => import('../views/Dashboard.vue') },
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/register', name: 'register', component: () => import('../views/Register.vue') },
    { path: '/shops', name: 'shops', component: () => import('../views/Shops.vue') },
    { path: '/products', name: 'products', component: () => import('../views/Products.vue') },
    { path: '/staffs', name: 'staffs', component: () => import('../views/Staffs.vue') },
  ],
})

export default router
