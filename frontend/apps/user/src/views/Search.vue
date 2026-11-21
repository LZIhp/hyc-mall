<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { http, BASE_URL } from '@hyc/request'

const router = useRouter()
const keyword = ref('')
const category = ref('')
const products = ref<any[]>([])
const loading = ref(false)
const categories = ['食品', '服装', '电子产品', '家居用品', '其他']

async function search() {
  loading.value = true
  try {
    const params: Record<string, string | number> = { page: 1, page_size: 20 }
    if (keyword.value) params.keyword = keyword.value
    if (category.value) params.category = category.value
    const res = await http.get('/api/products/', { params })
    products.value = res.data.results || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function resolveImage(image: string[] | null): string {
  if (image && image.length) {
    const url = image[0]
    return url.startsWith('http') ? url : `${BASE_URL}${url}`
  }
  return ''
}

onMounted(search)
</script>

<template>
  <div class="search">
    <header class="nav">
      <router-link to="/" class="back">←</router-link>
      <form class="searchbox" @submit.prevent="search">
        <input v-model="keyword" type="text" placeholder="搜索好物…" />
        <button type="submit">搜索</button>
      </form>
    </header>

    <div class="cats">
      <button class="cat" :class="{ active: category === '' }" @click="category = ''; search()">全部</button>
      <button
        v-for="c in categories"
        :key="c"
        class="cat"
        :class="{ active: category === c }"
        @click="category = c; search()"
      >{{ c }}</button>
    </div>

    <main v-if="products.length" class="list">
      <article
        v-for="p in products"
        :key="p.product_id"
        class="row"
        @click="router.push(`/product/${p.product_id}`)"
      >
        <img :src="resolveImage(p.image)" class="thumb" />
        <div class="info">
          <div class="name">{{ p.name }}</div>
          <div class="shop">{{ p.shop_name || '华耀城' }}</div>
          <div class="price">¥{{ p.price }}</div>
        </div>
      </article>
    </main>

    <div v-else-if="loading" class="state">搜索中…</div>
    <div v-else class="state">没有找到相关商品</div>
  </div>
</template>

<style scoped>
.search {
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
  font-size: 18px;
}

.searchbox {
  flex: 1;
  display: flex;
  background: var(--hyc-paper);
  border-radius: 999px;
  overflow: hidden;
}

.searchbox input {
  flex: 1;
  padding: 10px 16px;
  border: none;
  background: transparent;
  font-size: 14px;
  outline: none;
}

.searchbox button {
  padding: 0 18px;
  border: none;
  background: var(--hyc-amber);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
}

.cats {
  display: flex;
  gap: 8px;
  padding: 0 20px 14px;
  overflow-x: auto;
}

.cat {
  padding: 5px 14px;
  border: 1px solid #e5dccb;
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
}

.cat.active {
  background: var(--hyc-amber);
  border-color: var(--hyc-amber);
  color: #fff;
}

.list {
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.row {
  display: flex;
  gap: 12px;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 12px;
  cursor: pointer;
}

.thumb {
  width: 64px;
  height: 64px;
  border-radius: var(--hyc-radius-sm);
  object-fit: cover;
}

.info {
  flex: 1;
}

.name {
  font-size: 14px;
  font-weight: 600;
}

.shop {
  margin-top: 4px;
  color: var(--hyc-stone);
  font-size: 12px;
}

.price {
  margin-top: 6px;
  color: var(--hyc-cinnabar);
  font-size: 15px;
  font-weight: 700;
}

.state {
  padding: 80px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
