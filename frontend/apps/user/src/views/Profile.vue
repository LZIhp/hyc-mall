<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { http } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const user = ref<any>(null)
const loading = ref(true)

async function load() {
  if (!auth.token) {
    router.push('/login')
    return
  }
  loading.value = true
  try {
    const res = await http.get('/api/users/profile/')
    user.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

function changePassword() {
  const old_password = prompt('请输入旧密码')
  if (!old_password) return
  const new_password = prompt('请输入新密码（至少 8 位）')
  if (!new_password) return
  http
    .post('/api/users/change-password/', { old_password, new_password, new_password_confirm: new_password })
    .then(() => alert('密码修改成功'))
    .catch((e: any) => alert(e.response?.data?.old_password?.[0] || e.response?.data?.non_field_errors?.[0] || '修改失败'))
}

onMounted(load)
</script>

<template>
  <div class="profile">
    <header class="nav">
      <router-link to="/" class="back">← 返回</router-link>
      <h1 class="title">个人中心</h1>
      <button class="logout" @click="logout">退出</button>
    </header>

    <section v-if="user" class="card">
      <div class="avatar">{{ (user.username || '华')[0] }}</div>
      <div class="info">
        <div class="name">{{ user.username }}</div>
        <div class="row">📱 {{ user.phone_number || '未绑定' }}</div>
        <div class="row">✉ {{ user.email || '未设置' }}</div>
      </div>
    </section>

    <section class="menu">
      <button class="menu-item" @click="router.push('/favorites')">
        <span>♥ 我的收藏</span><span class="arrow">›</span>
      </button>
      <button class="menu-item" @click="changePassword">
        <span>🔒 修改密码</span><span class="arrow">›</span>
      </button>
    </section>

    <div v-if="loading && !user" class="state">加载中…</div>
  </div>
</template>

<style scoped>
.profile {
  max-width: 640px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
}

.back {
  color: var(--hyc-ink);
  text-decoration: none;
  font-size: 14px;
}

.title {
  flex: 1;
  font-family: var(--hyc-font-display);
  font-size: 18px;
  font-weight: 700;
}

.logout {
  border: none;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 13px;
  cursor: pointer;
}

.card {
  margin: 0 20px;
  display: flex;
  gap: 16px;
  align-items: center;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 20px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--hyc-amber);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--hyc-font-display);
  font-size: 24px;
}

.info .name {
  font-size: 17px;
  font-weight: 700;
}

.row {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.menu {
  margin: 20px;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  overflow: hidden;
}

.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  border: none;
  border-bottom: 1px solid #eee2cf;
  background: transparent;
  font-size: 14px;
  cursor: pointer;
  color: var(--hyc-ink);
}

.menu-item:last-child {
  border-bottom: none;
}

.arrow {
  color: var(--hyc-stone);
  font-size: 18px;
}

.state {
  padding: 80px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
