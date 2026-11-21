<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createClient } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const phone_number = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const client = createClient({ tokenKey: 'sjlocaltoken' })

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await client.post('/api/merchants/login/', {
      phone_number: phone_number.value,
      password: password.value,
    })
    auth.setToken(res.data.access)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.non_field_errors?.[0] || '登录失败，请检查账号密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="brand">华耀城 · 商家</h1>
      <p class="sub">登录商家工作台，管理你的店铺与商品</p>

      <form class="form" @submit.prevent="submit">
        <label class="field">
          <span>手机号</span>
          <input v-model="phone_number" type="tel" placeholder="请输入手机号" required />
        </label>
        <label class="field">
          <span>密码</span>
          <input v-model="password" type="password" placeholder="请输入密码" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="submit" :disabled="loading">{{ loading ? '登录中…' : '登录' }}</button>
      </form>

      <p class="switch">还没有商家账号？<router-link to="/register">立即入驻</router-link></p>
    </div>
  </div>
</template>

<style scoped>
.auth {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background:
    radial-gradient(ellipse at top right, rgba(185, 138, 60, 0.18), transparent 55%),
    linear-gradient(160deg, var(--hyc-ink) 0%, #2a241e 100%);
}

.auth-card {
  width: 100%;
  max-width: 380px;
  background: #fffdf8;
  border-radius: 20px;
  padding: 38px 32px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
}

.brand {
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
}

.sub {
  margin-top: 8px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
}

.field input {
  padding: 12px 14px;
  border: 1px solid #e5dccb;
  border-radius: var(--hyc-radius-sm);
  background: var(--hyc-cream);
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s var(--hyc-ease);
}

.field input:focus {
  border-color: var(--hyc-amber);
}

.error {
  color: var(--hyc-cinnabar);
  font-size: 13px;
}

.submit {
  padding: 13px;
  border: none;
  border-radius: var(--hyc-radius-sm);
  background: var(--hyc-amber);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.submit:disabled {
  opacity: 0.6;
}

.switch {
  margin-top: 22px;
  text-align: center;
  font-size: 13px;
  color: var(--hyc-stone);
}

.switch a {
  color: var(--hyc-amber);
  text-decoration: none;
}
</style>
