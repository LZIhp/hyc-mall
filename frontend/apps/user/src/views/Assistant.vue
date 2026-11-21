<script setup lang="ts">
import { ref } from 'vue'
import { http } from '@hyc/request'

const messages = ref<{ role: string; content: string }[]>([])
const input = ref('')
const sessionId = ref<number | null>(null)
const loading = ref(false)

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  try {
    const data: any = { message: text }
    if (sessionId.value) data.session_id = sessionId.value
    const res = await http.post('/api/ai/assistant/', data)
    sessionId.value = res.data.session_id
    messages.value.push({ role: 'assistant', content: res.data.reply })
    if (res.data.suggestions?.length) {
      messages.value.push({ role: 'assistant', content: '💡 ' + res.data.suggestions.join('；') })
    }
  } catch {
    messages.value.push({ role: 'assistant', content: '抱歉，助手暂时不可用，请稍后再试' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="assistant">
    <header class="nav">
      <router-link to="/" class="back">← 返回</router-link>
      <h1 class="title">购物助手</h1>
      <span class="placeholder"></span>
    </header>

    <main class="chat">
      <div v-if="!messages.length" class="empty">
        <div class="empty-mark">玉</div>
        <p>告诉我你想买什么，我帮你挑好物</p>
        <p class="empty-tip">例：给女朋友买生日礼物，预算 200</p>
      </div>

      <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.role">
        {{ m.content }}
      </div>

      <div v-if="loading" class="msg assistant">正在思考…</div>
    </main>

    <form class="inputbar" @submit.prevent="send">
      <input v-model="input" type="text" placeholder="描述你的需求…" />
      <button type="submit" :disabled="loading">发送</button>
    </form>
  </div>
</template>

<style scoped>
.assistant {
  max-width: 640px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav {
  display: flex;
  align-items: center;
  gap: 12px;
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
  font-size: 17px;
  text-align: center;
}

.placeholder {
  width: 40px;
}

.chat {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty {
  text-align: center;
  padding-top: 60px;
  color: var(--hyc-stone);
  font-size: 14px;
}

.empty-mark {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: var(--hyc-amber);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--hyc-font-display);
  font-size: 26px;
}

.empty-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #b3a68f;
}

.msg {
  max-width: 78%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.6;
}

.msg.user {
  align-self: flex-end;
  background: var(--hyc-amber);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.msg.assistant {
  align-self: flex-start;
  background: var(--hyc-paper);
  color: var(--hyc-ink);
  border-bottom-left-radius: 4px;
}

.inputbar {
  display: flex;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid #eee2cf;
  background: #fffdf8;
}

.inputbar input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e5dccb;
  border-radius: 999px;
  background: var(--hyc-cream);
  font-size: 14px;
  outline: none;
}

.inputbar button {
  padding: 0 22px;
  border: none;
  border-radius: 999px;
  background: var(--hyc-amber);
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.inputbar button:disabled {
  opacity: 0.6;
}
</style>
