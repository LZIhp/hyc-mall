<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { createClient } from '@hyc/request'

const client = createClient({ tokenKey: 'adtoken' })
const shops = ref<any[]>([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const res = await client.get('/api/admins/pending-shops/')
    shops.value = res.data.pending_shops || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function review(shop: any, status: string) {
  try {
    await client.patch(`/api/shops/${shop.shop_id}/review/`, { status })
    shops.value = shops.value.filter((s) => s.shop_id !== shop.shop_id)
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

<template>
  <div class="shops">
    <h1 class="title">店铺审核</h1>
    <p class="sub">共 {{ shops.length }} 家店铺待审核</p>

    <main v-if="shops.length" class="list">
      <article v-for="s in shops" :key="s.shop_id" class="card">
        <div class="card-head">
          <h3 class="name">{{ s.name }}</h3>
        </div>
        <p class="info">📍 {{ s.address }}</p>
        <p class="info">☏ {{ s.phone_number }}</p>
        <p class="info">商家：{{ s.merchant_name }}（{{ s.merchant_phone }}）</p>
        <div class="actions">
          <button class="btn btn--ok" @click="review(s, 'approved')">通过</button>
          <button class="btn btn--no" @click="review(s, 'rejected')">拒绝</button>
        </div>
      </article>
    </main>

    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">没有待审核的店铺</div>
  </div>
</template>

<style scoped>
.shops {
  max-width: 720px;
}

.title {
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
}

.sub {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.list {
  margin-top: 20px;
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

.name {
  font-size: 16px;
  font-weight: 700;
}

.info {
  margin-top: 8px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.actions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 999px;
  font-size: 14px;
  cursor: pointer;
}

.btn--ok {
  background: var(--hyc-amber);
  color: #fff;
}

.btn--no {
  background: transparent;
  border: 1px solid var(--hyc-cinnabar);
  color: var(--hyc-cinnabar);
}

.state {
  padding: 60px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
