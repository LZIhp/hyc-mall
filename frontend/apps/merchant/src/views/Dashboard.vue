<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createClient } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const merchant = ref<any>(null)
const shopCount = ref(0)
const productCount = ref(0)

const client = createClient({ tokenKey: 'sjlocaltoken' })

async function load() {
  try {
    const [mRes, sRes, pRes] = await Promise.all([
      client.get('/api/merchants/profile/'),
      client.get('/api/shops/', { params: { page_size: 1 } }),
      client.get('/api/products/', { params: { page_size: 1 } }),
    ])
    merchant.value = mRes.data
    shopCount.value = sRes.data.count || 0
    productCount.value = pRes.data.count || 0
  } catch (e) {
    console.error(e)
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  if (!auth.token) {
    router.push('/login')
    return
  }
  load()
})
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">华</div>
        <div>
          <div class="brand-name">华耀城</div>
          <div class="brand-sub">商家工作台</div>
        </div>
      </div>
      <nav class="menu">
        <router-link to="/" class="menu-item active">⌂ 工作台</router-link>
        <router-link to="/shops" class="menu-item">▣ 店铺管理</router-link>
        <router-link to="/products" class="menu-item">◫ 商品管理</router-link>
        <router-link to="/staffs" class="menu-item">◉ 员工管理</router-link>
      </nav>
      <button class="logout" @click="logout">退出登录</button>
    </aside>

    <main class="content">
      <header class="topbar">
        <h1 class="hello">{{ merchant?.name || '商家' }}，欢迎回来</h1>
        <span v-if="merchant?.phone_number" class="phone">☏ {{ merchant.phone_number }}</span>
      </header>

      <section class="stats">
        <div class="stat">
          <div class="stat-num">{{ shopCount }}</div>
          <div class="stat-label">我的店铺</div>
        </div>
        <div class="stat">
          <div class="stat-num">{{ productCount }}</div>
          <div class="stat-label">在售商品</div>
        </div>
      </section>

      <section class="actions">
        <h2 class="section-title">快捷操作</h2>
        <div class="grid">
          <button class="action" @click="router.push('/shops')">＋ 注册店铺</button>
          <button class="action" @click="router.push('/products')">＋ 添加商品</button>
          <button class="action" @click="router.push('/staffs')">＋ 添加员工</button>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: linear-gradient(180deg, var(--hyc-ink) 0%, #14110e 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 0 8px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--hyc-amber), #8a6428);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--hyc-font-display);
  font-size: 20px;
}

.brand-name {
  font-family: var(--hyc-font-display);
  font-size: 17px;
  font-weight: 700;
}

.brand-sub {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.55);
}

.menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 20px;
}

.menu-item {
  padding: 12px 14px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s var(--hyc-ease);
}

.menu-item:hover,
.menu-item.active {
  background: rgba(185, 138, 60, 0.22);
  color: var(--hyc-amber-soft);
}

.logout {
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  cursor: pointer;
}

.logout:hover {
  color: #fff;
}

.content {
  flex: 1;
  margin-left: 220px;
  padding: 32px 40px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hello {
  font-family: var(--hyc-font-display);
  font-size: 26px;
  font-weight: 700;
}

.phone {
  color: var(--hyc-stone);
  font-size: 14px;
}

.stats {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  max-width: 480px;
}

.stat {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 24px;
  box-shadow: var(--hyc-shadow);
}

.stat-num {
  font-family: var(--hyc-font-display);
  font-size: 36px;
  font-weight: 700;
  color: var(--hyc-amber);
}

.stat-label {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.actions {
  margin-top: 32px;
}

.section-title {
  font-family: var(--hyc-font-display);
  font-size: 17px;
}

.grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  max-width: 640px;
}

.action {
  padding: 22px;
  border: 1px dashed #d5c8ae;
  border-radius: var(--hyc-radius);
  background: transparent;
  color: var(--hyc-amber);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s var(--hyc-ease);
}

.action:hover {
  border-color: var(--hyc-amber);
  background: var(--hyc-amber-soft);
}
</style>
