<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { http } from '@hyc/request'

const router = useRouter()
const form = ref({
  username: '',
  phone_number: '',
  email: '',
  password: '',
  password_confirm: '',
})
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await http.post('/api/users/register/', form.value)
    router.push('/login')
  } catch (e: any) {
    const data = e.response?.data
    error.value = Object.values(data || {}).flat().join('；') || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth">
    <div class="auth-card">
      <router-link to="/login" class="back">← 返回登录</router-link>
      <h1 class="auth-title">创建账号</h1>
      <p class="auth-sub">加入华耀城，收藏心仪好物</p>

      <form class="auth-form" @submit.prevent="submit">
        <label class="field">
          <span>用户名</span>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </label>
        <label class="field">
          <span>手机号</span>
          <input v-model="form.phone_number" type="tel" placeholder="11 位手机号" required />
        </label>
        <label class="field">
          <span>邮箱</span>
          <input v-model="form.email" type="email" placeholder="请输入邮箱" required />
        </label>
        <label class="field">
          <span>密码</span>
          <input v-model="form.password" type="password" placeholder="至少 8 位，含字母和数字" required />
        </label>
        <label class="field">
          <span>确认密码</span>
          <input v-model="form.password_confirm" type="password" placeholder="再次输入密码" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="submit" :disabled="loading">{{ loading ? '注册中…' : '注册' }}</button>
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
  margin-top: 26px;
  display: flex;
  flex-direction: column;
  gap: 15px;
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
</style>
