<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { createClient } from '@hyc/request'

const client = createClient({ tokenKey: 'adtoken' })
const users = ref<any[]>([])
const loading = ref(true)
const currentPage = ref(1)
const totalCount = ref(0)

async function load(page = 1) {
  loading.value = true
  try {
    const res = await client.get('/api/admins/users/', { params: { page } })
    users.value = res.data.results || []
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

async function toggle(u: any) {
  try {
    await client.patch(`/api/admins/users/${u.id}/`, { is_active: !u.is_active })
    u.is_active = !u.is_active
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

<template>
  <div class="users">
    <h1 class="title">用户管理</h1>

    <main v-if="users.length" class="list">
      <article v-for="u in users" :key="u.id" class="row">
        <div class="info">
          <div class="name">{{ u.username }}</div>
          <div class="meta">{{ u.phone_number || '未绑定手机号' }} · {{ u.email || '未设置邮箱' }}</div>
        </div>
        <button class="toggle" :class="{ on: u.is_active }" @click="toggle(u)">
          {{ u.is_active ? '正常' : '已禁用' }}
        </button>
      </article>
    </main>

    <div v-if="totalPages > 1" class="pager">
      <button class="pager-btn" :disabled="currentPage <= 1" @click="prevPage">上一页</button>
      <span class="pager-info">{{ currentPage }} / {{ totalPages }} · 共 {{ totalCount }} 条</span>
      <button class="pager-btn" :disabled="currentPage >= totalPages" @click="nextPage">下一页</button>
    </div>

    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">暂无用户</div>
  </div>
</template>

<style scoped>
.users {
  max-width: 720px;
}

.title {
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
}

.list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.row {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 14px 16px;
}

.info {
  flex: 1;
}

.name {
  font-size: 15px;
  font-weight: 600;
}

.meta {
  margin-top: 4px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.toggle {
  padding: 6px 16px;
  border: 1px solid #d5c8ae;
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 13px;
  cursor: pointer;
}

.toggle.on {
  border-color: #3a7d44;
  color: #3a7d44;
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
  border: 1px solid var(--hyc-cinnabar);
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-cinnabar);
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
