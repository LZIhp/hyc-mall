<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createClient } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const stats = ref<any>(null)

const client = createClient({ tokenKey: 'adtoken' })

async function load() {
  try {
    const res = await client.get('/api/admins/dashboard/')
    stats.value = res.data
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
          <div class="brand-sub">运营管理后台</div>
        </div>
      </div>
      <nav class="menu">
        <router-link to="/" class="menu-item active">⌂ 数据看板</router-link>
        <router-link to="/shops" class="menu-item">◈ 店铺审核</router-link>
        <router-link to="/products" class="menu-item">◫ 商品监管</router-link>
        <router-link to="/users" class="menu-item">◉ 用户管理</router-link>
        <router-link to="/merchants" class="menu-item">▣ 商家管理</router-link>
      </nav>
      <button class="logout" @click="logout">退出登录</button>
    </aside>

    <main class="content">
      <h1 class="title">数据看板</h1>

      <section v-if="stats" class="stats">
        <div class="stat">
          <div class="stat-num">{{ stats.shop_count }}</div>
          <div class="stat-label">店铺总数</div>
        </div>
        <div class="stat stat--warn">
          <div class="stat-num">{{ stats.pending_shop_count }}</div>
          <div class="stat-label">待审核店铺</div>
        </div>
        <div class="stat">
          <div class="stat-num">{{ stats.product_count }}</div>
          <div class="stat-label">商品总数</div>
        </div>
        <div class="stat">
          <div class="stat-num">{{ stats.user_count }}</div>
          <div class="stat-label">注册用户</div>
        </div>
        <div class="stat">
          <div class="stat-num">{{ stats.merchant_count }}</div>
          <div class="stat-label">入驻商家</div>
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
  background: linear-gradient(180deg, #14110e 0%, #0e0c0a 100%);
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
  background: linear-gradient(135deg, var(--hyc-cinnabar), #7e241b);
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
  background: rgba(192, 57, 43, 0.25);
  color: #f0c4bc;
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

.title {
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
}

.stats {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  max-width: 720px;
}

.stat {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 24px;
  box-shadow: var(--hyc-shadow);
}

.stat--warn {
  background: #f8e3df;
}

.stat-num {
  font-family: var(--hyc-font-display);
  font-size: 34px;
  font-weight: 700;
  color: var(--hyc-cinnabar);
}

.stat-label {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}
</style>
