<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { http, BASE_URL } from '@hyc/request'

interface Product {
  product_id: number
  name: string
  price: string
  description?: string
  category?: string
  image: string[] | null
  shop?: number
  shop_name?: string
}

interface Shop {
  shop_id: number
  name: string
  address?: string
  phone_number?: string
  description?: string
}

const route = useRoute()
const router = useRouter()
const product = ref<Product | null>(null)
const shop = ref<Shop | null>(null)
const loading = ref(true)
const favoriting = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await http.get(`/api/products/${route.params.id}/`)
    product.value = res.data
    const shopId = res.data.shop
    if (shopId) {
      const shopRes = await http.get(`/api/shops/${shopId}/`)
      shop.value = shopRes.data
    }
  } catch (e) {
    console.error('加载商品失败', e)
  } finally {
    loading.value = false
  }
}

function resolveImage(image: Product['image']): string {
  if (image && image.length) {
    const url = image[0]
    return url.startsWith('http') ? url : `${BASE_URL}${url}`
  }
  return ''
}

async function toggleFavorite() {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  favoriting.value = true
  try {
    await http.post('/api/users/favorites/', { product: product.value?.product_id })
    alert('收藏成功')
  } catch (e: any) {
    const data = e.response?.data
    alert(data?.product?.[0] || data?.non_field_errors?.[0] || '收藏失败')
  } finally {
    favoriting.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-if="product" class="detail">
    <header class="nav">
      <router-link to="/" class="back">← 返回</router-link>
      <button class="fav" :disabled="favoriting" @click="toggleFavorite">
        {{ favoriting ? '收藏中…' : '♥ 收藏' }}
      </button>
    </header>

    <img :src="resolveImage(product.image)" class="hero-img" :alt="product.name" />

    <div class="body">
      <div class="meta">
        <span class="category">{{ product.category || '好物' }}</span>
        <h1 class="title">{{ product.name }}</h1>
        <div class="price">¥{{ product.price }}</div>
      </div>

      <p v-if="product.description" class="desc">{{ product.description }}</p>

      <section v-if="shop" class="shop-card" @click="router.push(`/shop/${shop.shop_id}`)">
        <div class="shop-head">
          <div>
            <div class="shop-name">{{ shop.name }}</div>
            <div class="shop-addr">{{ shop.address || '地址未填写' }}</div>
          </div>
          <span class="shop-arrow">›</span>
        </div>
        <div v-if="shop.phone_number" class="shop-phone">☏ {{ shop.phone_number }}</div>
      </section>
    </div>
  </div>

  <div v-else-if="loading" class="state">加载中…</div>
  <div v-else class="state">商品不存在</div>
</template>

<style scoped>
.detail {
  max-width: 640px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
}

.back {
  color: var(--hyc-ink);
  text-decoration: none;
  font-size: 14px;
}

.fav {
  padding: 7px 16px;
  border: 1px solid var(--hyc-cinnabar);
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-cinnabar);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s var(--hyc-ease);
}

.fav:hover {
  background: var(--hyc-cinnabar);
  color: #fff;
}

.hero-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  display: block;
}

.body {
  padding: 20px;
}

.category {
  display: inline-block;
  padding: 3px 10px;
  background: var(--hyc-amber-soft);
  color: var(--hyc-amber);
  border-radius: 999px;
  font-size: 12px;
}

.title {
  margin-top: 12px;
  font-family: var(--hyc-font-display);
  font-size: 24px;
  font-weight: 700;
  line-height: 1.4;
}

.price {
  margin-top: 12px;
  color: var(--hyc-cinnabar);
  font-size: 26px;
  font-weight: 700;
}

.desc {
  margin-top: 18px;
  color: var(--hyc-stone);
  font-size: 14px;
  line-height: 1.7;
}

.shop-card {
  margin-top: 24px;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s var(--hyc-ease);
}

.shop-card:hover {
  transform: translateY(-2px);
}

.shop-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.shop-name {
  font-weight: 600;
  font-size: 15px;
}

.shop-addr {
  margin-top: 4px;
  color: var(--hyc-stone);
  font-size: 13px;
}

.shop-arrow {
  color: var(--hyc-stone);
  font-size: 22px;
}

.shop-phone {
  margin-top: 10px;
  color: var(--hyc-amber);
  font-size: 13px;
}

.state {
  padding: 100px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
