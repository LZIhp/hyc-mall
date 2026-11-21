<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { createClient } from '@hyc/request'

const client = createClient({ tokenKey: 'sjlocaltoken' })
const shops = ref<any[]>([])
const loading = ref(true)
const showForm = ref(false)
const currentPage = ref(1)
const totalCount = ref(0)
const form = ref({
  name: '',
  address: '',
  phone_number: '',
  description: '',
  latitude: 0,
  longitude: 0,
})

async function load(page = 1) {
  loading.value = true
  try {
    const res = await client.get('/api/shops/', { params: { page } })
    shops.value = res.data.results || []
    totalCount.value = res.data.count || 0
    currentPage.value = page
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const totalPages = computed(() => Math.ceil(totalCount.value / 10))

function prevPage() {
  if (currentPage.value > 1) load(currentPage.value - 1)
}

function nextPage() {
  if (currentPage.value < totalPages.value) load(currentPage.value + 1)
}

function locate() {
  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition((pos) => {
    form.value.latitude = Number(pos.coords.latitude.toFixed(6))
    form.value.longitude = Number(pos.coords.longitude.toFixed(6))
    alert('位置已获取')
  })
}

async function submit() {
  try {
    await client.post('/api/shops/', form.value)
    alert('店铺提交成功，等待审核')
    showForm.value = false
    load()
  } catch (e: any) {
    alert(Object.values(e.response?.data || {}).flat().join('；') || '提交失败')
  }
}

const statusText: Record<string, string> = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已拒绝',
  suspended: '已暂停',
}

onMounted(load)
</script>

<template>
  <div class="shops">
    <header class="head">
      <h1 class="title">店铺管理</h1>
      <button class="btn" @click="showForm = !showForm">{{ showForm ? '取消' : '＋ 注册店铺' }}</button>
    </header>

    <form v-if="showForm" class="form" @submit.prevent="submit">
      <input v-model="form.name" type="text" placeholder="店铺名称" required />
      <input v-model="form.address" type="text" placeholder="店铺地址" required />
      <input v-model="form.phone_number" type="tel" placeholder="联系电话" required />
      <textarea v-model="form.description" rows="3" placeholder="店铺简介（可选）"></textarea>
      <div class="loc">
        <button type="button" class="loc-btn" @click="locate">📍 获取位置</button>
        <span>经 {{ form.longitude }} / 纬 {{ form.latitude }}</span>
      </div>
      <button class="submit" type="submit">提交注册</button>
    </form>

    <main v-if="shops.length" class="list">
      <article v-for="s in shops" :key="s.shop_id" class="card">
        <div class="card-head">
          <h3 class="name">{{ s.name }}</h3>
          <span class="status" :class="s.status">{{ statusText[s.status] || s.status }}</span>
        </div>
        <p class="addr">📍 {{ s.address }}</p>
        <p class="phone">☏ {{ s.phone_number }}</p>
      </article>
    </main>

    <div v-if="totalPages > 1" class="pager">
      <button class="pager-btn" :disabled="currentPage <= 1" @click="prevPage">上一页</button>
      <span class="pager-info">{{ currentPage }} / {{ totalPages }} · 共 {{ totalCount }} 条</span>
      <button class="pager-btn" :disabled="currentPage >= totalPages" @click="nextPage">下一页</button>
    </div>

    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">还没有店铺，点击右上角注册</div>
  </div>
</template>

<style scoped>
.shops {
  max-width: 720px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.title {
  font-family: var(--hyc-font-display);
  font-size: 22px;
}

.btn {
  padding: 9px 18px;
  border: none;
  border-radius: 999px;
  background: var(--hyc-amber);
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.form {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.form input,
.form textarea {
  padding: 11px 14px;
  border: 1px solid #e5dccb;
  border-radius: var(--hyc-radius-sm);
  background: #fffdf8;
  font-size: 14px;
  outline: none;
  font-family: inherit;
}

.loc {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--hyc-stone);
}

.loc-btn {
  padding: 7px 14px;
  border: 1px solid var(--hyc-amber);
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-amber);
  font-size: 13px;
  cursor: pointer;
}

.submit {
  padding: 12px;
  border: none;
  border-radius: var(--hyc-radius-sm);
  background: var(--hyc-amber);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.card {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 18px;
  box-shadow: var(--hyc-shadow);
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.name {
  font-size: 16px;
  font-weight: 700;
}

.status {
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.status.pending {
  background: #f5e6c8;
  color: #a06a1f;
}

.status.approved {
  background: #dcecdc;
  color: #3a7d44;
}

.status.rejected {
  background: #f6d8d5;
  color: #b03024;
}

.status.suspended {
  background: #e2e0dc;
  color: #6b655e;
}

.addr,
.phone {
  margin-top: 8px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.state {
  padding: 60px 0;
  text-align: center;
  color: var(--hyc-stone);
}

.pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 20px 0;
}

.pager-btn {
  padding: 8px 18px;
  border: 1px solid var(--hyc-amber);
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-amber);
  font-size: 13px;
  cursor: pointer;
}

.pager-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pager-info {
  color: var(--hyc-stone);
  font-size: 13px;
}
</style>
