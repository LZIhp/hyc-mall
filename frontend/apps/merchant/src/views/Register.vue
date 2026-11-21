<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createClient } from '@hyc/request'

const router = useRouter()
const form = ref({ name: '', phone_number: '', email: '', password: '', password_confirm: '' })
const error = ref('')
const loading = ref(false)

const client = createClient()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await client.post('/api/merchants/register/', form.value)
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
      <h1 class="brand">商家入驻</h1>
      <p class="sub">加入华耀城，开启你的经营之旅</p>

      <form class="form" @submit.prevent="submit">
        <label class="field">
          <span>商家名称</span>
          <input v-model="form.name" type="text" placeholder="请输入商家名称" required />
        </label>
        <label class="field">
          <span>联系电话</span>
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
        <button class="submit" :disabled="loading">{{ loading ? '入驻中…' : '立即入驻' }}</button>
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
    radial-gradient(ellipse at top right, rgba(185, 138, 60, 0.18), transparent 55%),
    linear-gradient(160deg, var(--hyc-ink) 0%, #2a241e 100%);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: #fffdf8;
  border-radius: 20px;
  padding: 36px 32px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
}

.back {
  color: var(--hyc-stone);
  text-decoration: none;
  font-size: 13px;
}

.brand {
  margin-top: 18px;
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
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
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
</style>
