<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { http } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const phone_number = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await http.post('/api/users/login/', {
      phone_number: phone_number.value,
      password: password.value,
    })
    auth.setToken(res.data.access)
    router.push('/')
  } catch (e: any) {
    const data = e.response?.data
    error.value = data?.non_field_errors?.[0] || data?.detail || '登录失败，请检查账号密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth">
    <div class="auth-card">
      <router-link to="/" class="back">← 返回</router-link>
      <h1 class="auth-title">欢迎回来</h1>
      <p class="auth-sub">登录华耀城，继续发现好物</p>

      <form class="auth-form" @submit.prevent="submit">
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

      <p class="switch">还没有账号？<router-link to="/register">立即注册</router-link></p>
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
  background: linear-gradient(160deg, var(--hyc-cream) 0%, var(--hyc-paper) 100%);
}

.auth-card {
  width: 100%;
  max-width: 380px;
  background: #fffdf8;
  border-radius: 20px;
  padding: 36px 32px;
  box-shadow: var(--hyc-shadow-lg);
}

.back {
  color: var(--hyc-stone);
  text-decoration: none;
  font-size: 13px;
}

.auth-title {
  margin-top: 20px;
  font-family: var(--hyc-font-display);
  font-size: 26px;
  font-weight: 700;
}

.auth-sub {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.auth-form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: var(--hyc-ink);
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
  transition: opacity 0.2s var(--hyc-ease);
}

.submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit:hover:not(:disabled) {
  opacity: 0.9;
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
