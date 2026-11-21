<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createClient } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const client = createClient({ tokenKey: 'adtoken' })

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await client.post('/api/admins/login/', { username: username.value, password: password.value })
    auth.setToken(res.data.access)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.non_field_errors?.[0] || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="brand">华耀城 · 管理端</h1>
      <p class="sub">平台运营管理后台</p>

      <form class="form" @submit.prevent="submit">
        <label class="field">
          <span>管理员账号</span>
          <input v-model="username" type="text" placeholder="请输入用户名" required />
        </label>
        <label class="field">
          <span>密码</span>
          <input v-model="password" type="password" placeholder="请输入密码" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="submit" :disabled="loading">{{ loading ? '登录中…' : '登录' }}</button>
      </form>
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
    radial-gradient(ellipse at top left, rgba(192, 57, 43, 0.2), transparent 50%),
    linear-gradient(160deg, #14110e 0%, #1c1917 100%);
}

.auth-card {
  width: 100%;
  max-width: 380px;
  background: #fffdf8;
  border-radius: 20px;
  padding: 38px 32px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
}

.brand {
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
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
}

.field input:focus {
  border-color: var(--hyc-cinnabar);
}

.error {
  color: var(--hyc-cinnabar);
  font-size: 13px;
}

.submit {
  padding: 13px;
  border: none;
  border-radius: var(--hyc-radius-sm);
  background: var(--hyc-cinnabar);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.submit:disabled {
  opacity: 0.6;
}
</style>
