import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/Home.vue') },
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/register', name: 'register', component: () => import('../views/Register.vue') },
    { path: '/search', name: 'search', component: () => import('../views/Search.vue') },
    { path: '/product/:id', name: 'product', component: () => import('../views/ProductDetail.vue') },
    { path: '/shop/:id', name: 'shop', component: () => import('../views/ShopDetail.vue') },
    { path: '/favorites', name: 'favorites', component: () => import('../views/Favorites.vue') },
    { path: '/profile', name: 'profile', component: () => import('../views/Profile.vue') },
    { path: '/assistant', name: 'assistant', component: () => import('../views/Assistant.vue') },
  ],
})

export default router
