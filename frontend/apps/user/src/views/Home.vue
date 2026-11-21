<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { http, BASE_URL } from '@hyc/request'
import { useAuthStore } from '../stores/auth'

interface Product {
  product_id: number
  name: string
  price: string
  image: string[] | null
  shop_name?: string
  shop_id?: number
  description?: string
}

const router = useRouter()
const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)

function logout() {
  auth.logout()
}

const products = ref<Product[]>([])
const loading = ref(true)
const loadingMore = ref(false)
const currentPage = ref(1)
const totalCount = ref(0)

const hasMore = computed(() => products.value.length < totalCount.value)

const columns = computed(() => {
  const cols: Product[][] = [[], []]
  products.value.forEach((p, i) => cols[i % 2].push(p))
  return cols
})

function resolveImage(image: Product['image']): string {
  if (image && image.length) {
    const url = image[0]
    return url.startsWith('http') ? url : `${BASE_URL}${url}`
  }
  return ''
}

async function fetchProducts(page: number) {
  try {
    const res = await http.get('/api/products/', { params: { page } })
    const list = res.data.results || []
    products.value = page === 1 ? list : [...products.value, ...list]
    totalCount.value = res.data.count || 0
    currentPage.value = page
  } catch (e) {
    console.error('加载商品失败', e)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

async function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  await fetchProducts(currentPage.value + 1)
}

function onScroll() {
  const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 300
  if (nearBottom) loadMore()
}

function goDetail(p: Product) {
  router.push(`/product/${p.product_id}`)
}

onMounted(() => {
  fetchProducts(1)
  window.addEventListener('scroll', onScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <div class="home">
    <header class="nav">
      <div class="nav-brand">华耀城</div>
      <nav class="nav-actions">
        <a href="http://localhost:5174/login" class="nav-link">成为商家</a>
        <router-link to="/assistant" class="nav-link">助手</router-link>
        <router-link to="/favorites" class="nav-link">收藏</router-link>
        <router-link v-if="!isLoggedIn" to="/login" class="nav-link nav-link--primary">登录</router-link>
        <button v-else class="nav-link nav-link--primary logout-btn" @click="logout">退出登录</button>
      </nav>
    </header>

    <section class="hero">
      <h1 class="hero-title">发现生活的好物</h1>
      <p class="hero-sub">温暖每一处日常</p>
      <div class="hero-rule"></div>
    </section>

    <main v-if="!loading && products.length" class="grid">
      <div v-for="(col, i) in columns" :key="i" class="col">
        <article
          v-for="item in col"
          :key="item.product_id"
          class="card"
          @click="goDetail(item)"
        >
          <img :src="resolveImage(item.image)" class="card-img" :alt="item.name" />
          <div class="card-info">
            <h3 class="card-title">{{ item.name }}</h3>
            <p class="card-shop">{{ item.shop_name || '华耀城' }}</p>
            <div class="card-price">¥{{ item.price }}</div>
          </div>
        </article>
      </div>
    </main>

    <div v-if="loadingMore" class="state">正在加载更多…</div>
    <div v-else-if="products.length && !hasMore" class="state">已经到底啦</div>
    <div v-else-if="loading" class="state">正在拾取好物…</div>
    <div v-else class="state">暂无商品，稍后再来看看</div>
  </div>
</template>

<style scoped>
.home {
  max-width: 640px;
  margin: 0 auto;
  padding: 0 20px 40px;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
}

.nav-brand {
  font-family: var(--hyc-font-display);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 2px;
}

.nav-actions {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-link {
  color: var(--hyc-ink);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s var(--hyc-ease);
}

.nav-link:hover {
  color: var(--hyc-amber);
}

.nav-link--primary {
  padding: 6px 16px;
  border: 1px solid var(--hyc-amber);
  border-radius: 999px;
  color: var(--hyc-amber);
}

.logout-btn {
  background: transparent;
  cursor: pointer;
  font-size: 14px;
}

.hero {
  padding: 40px 0 28px;
}

.hero-title {
  font-family: var(--hyc-font-display);
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 1px;
}

.hero-sub {
  margin-top: 8px;
  color: var(--hyc-stone);
  font-size: 14px;
}

.hero-rule {
  margin-top: 20px;
  width: 48px;
  height: 2px;
  background: var(--hyc-amber);
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--hyc-shadow);
  transition: transform 0.3s var(--hyc-ease), box-shadow 0.3s var(--hyc-ease);
  animation: rise 0.5s var(--hyc-ease) both;
}

.card:nth-child(2n) {
  animation-delay: 0.08s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--hyc-shadow-lg);
}

.card-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  display: block;
}

.card-info {
  padding: 14px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-shop {
  margin-top: 6px;
  font-size: 12px;
  color: var(--hyc-stone);
}

.card-price {
  margin-top: 8px;
  color: var(--hyc-cinnabar);
  font-size: 16px;
  font-weight: 700;
}

.state {
  padding: 80px 0;
  text-align: center;
  color: var(--hyc-stone);
  font-size: 14px;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
