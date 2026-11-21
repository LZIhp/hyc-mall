<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { http, BASE_URL } from '@hyc/request'

interface Shop {
  shop_id: number
  name: string
  address?: string
  phone_number?: string
  description?: string
  photo?: string | null
}

const route = useRoute()
const router = useRouter()
const shop = ref<Shop | null>(null)
const products = ref<any[]>([])
const loading = ref(true)

function resolveImage(image: string[] | string | null): string {
  if (!image) return ''
  const url = Array.isArray(image) ? image[0] : image
  return url.startsWith('http') ? url : `${BASE_URL}${url}`
}

async function load() {
  loading.value = true
  try {
    const id = route.params.id
    const [shopRes, prodRes] = await Promise.all([
      http.get(`/api/shops/${id}/`),
      http.get(`/api/shops/${id}/products/`),
    ])
    shop.value = shopRes.data
    products.value = prodRes.data.results || prodRes.data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-if="shop" class="shop">
    <header class="nav">
      <router-link to="/" class="back">← 返回</router-link>
      <h1 class="nav-title">{{ shop.name }}</h1>
      <span class="placeholder"></span>
    </header>

    <section class="head">
      <div class="avatar">{{ shop.name.slice(0, 1) }}</div>
      <div class="meta">
        <div class="name">{{ shop.name }}</div>
        <div class="addr">{{ shop.address || '地址未填写' }}</div>
        <div v-if="shop.phone_number" class="phone">☏ {{ shop.phone_number }}</div>
      </div>
    </section>

    <p v-if="shop.description" class="desc">{{ shop.description }}</p>

    <h2 class="section-title">店内好物</h2>
    <main v-if="products.length" class="grid">
      <article
        v-for="p in products"
        :key="p.product_id"
        class="card"
        @click="router.push(`/product/${p.product_id}`)"
      >
        <img :src="resolveImage(p.image)" class="card-img" />
        <div class="card-info">
          <div class="card-name">{{ p.name }}</div>
          <div class="card-price">¥{{ p.price }}</div>
        </div>
      </article>
    </main>
    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">暂无商品</div>
  </div>

  <div v-else class="state">店铺不存在</div>
</template>

<style scoped>
.shop {
  max-width: 640px;
  margin: 0 auto;
  padding-bottom: 40px;
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

.nav-title {
  flex: 1;
  font-family: var(--hyc-font-display);
  font-size: 16px;
  text-align: center;
}

.placeholder {
  width: 40px;
}

.head {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 8px 20px 20px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--hyc-amber);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--hyc-font-display);
  font-size: 28px;
}

.meta .name {
  font-size: 18px;
  font-weight: 700;
}

.addr {
  margin-top: 6px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.phone {
  margin-top: 4px;
  color: var(--hyc-amber);
  font-size: 13px;
}

.desc {
  padding: 0 20px 20px;
  color: var(--hyc-stone);
  font-size: 14px;
  line-height: 1.7;
}

.section-title {
  padding: 0 20px 14px;
  font-family: var(--hyc-font-display);
  font-size: 17px;
}

.grid {
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.card {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  overflow: hidden;
  cursor: pointer;
}

.card-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
}

.card-info {
  padding: 10px 12px;
}

.card-name {
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-price {
  margin-top: 6px;
  color: var(--hyc-cinnabar);
  font-size: 14px;
  font-weight: 700;
}

.state {
  padding: 80px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
