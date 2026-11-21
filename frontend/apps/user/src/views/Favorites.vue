<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { http, BASE_URL } from '@hyc/request'

interface FavoriteItem {
  favorite_id: number
  category: string | null
  note: string | null
  product_detail: {
    product_id: number
    name: string
    price: string
    image: string[] | null
  } | null
}

const router = useRouter()
const items = ref<FavoriteItem[]>([])
const loading = ref(true)
const selected = ref<number[]>([])
const filterCategory = ref('')

const categories = computed(() => {
  const set = new Set<string>()
  items.value.forEach((i) => i.category && set.add(i.category))
  return Array.from(set)
})

const filtered = computed(() => {
  if (!filterCategory.value) return items.value
  return items.value.filter((i) => i.category === filterCategory.value)
})

function resolveImage(image: string[] | null | undefined): string {
  if (image && image.length) {
    const url = image[0]
    return url.startsWith('http') ? url : `${BASE_URL}${url}`
  }
  return ''
}

async function load() {
  loading.value = true
  try {
    const res = await http.get('/api/users/favorites/', { params: { page_size: 100 } })
    items.value = res.data.results || []
  } catch (e) {
    console.error('加载收藏失败', e)
  } finally {
    loading.value = false
  }
}

function toggleSelect(id: number) {
  const idx = selected.value.indexOf(id)
  if (idx >= 0) selected.value.splice(idx, 1)
  else selected.value.push(id)
}

async function removeOne(id: number) {
  try {
    await http.delete(`/api/users/favorites/${id}/`)
    items.value = items.value.filter((i) => i.favorite_id !== id)
  } catch (e) {
    console.error(e)
  }
}

async function batchRemove() {
  if (!selected.value.length) return
  if (!confirm(`确定删除选中的 ${selected.value.length} 条收藏吗？`)) return
  try {
    await http.post('/api/users/favorites/batch-delete/', { ids: selected.value })
    items.value = items.value.filter((i) => !selected.value.includes(i.favorite_id))
    selected.value = []
  } catch (e) {
    console.error(e)
  }
}

async function editCategory(item: FavoriteItem) {
  const cat = prompt('设置分类（如：想买 / 生日礼物）', item.category || '')
  if (cat === null) return
  try {
    await http.patch(`/api/users/favorites/${item.favorite_id}/`, { category: cat })
    item.category = cat || null
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

<template>
  <div class="favs">
    <header class="nav">
      <router-link to="/" class="back">← 返回</router-link>
      <h1 class="title">我的收藏</h1>
      <button v-if="selected.length" class="batch" @click="batchRemove">删除({{ selected.length }})</button>
      <span v-else class="placeholder"></span>
    </header>

    <div v-if="categories.length" class="filters">
      <button
        class="chip"
        :class="{ active: filterCategory === '' }"
        @click="filterCategory = ''"
      >全部</button>
      <button
        v-for="c in categories"
        :key="c"
        class="chip"
        :class="{ active: filterCategory === c }"
        @click="filterCategory = c"
      >{{ c }}</button>
    </div>

    <main v-if="filtered.length" class="list">
      <article v-for="item in filtered" :key="item.favorite_id" class="row">
        <label class="check">
          <input type="checkbox" :checked="selected.includes(item.favorite_id)" @change="toggleSelect(item.favorite_id)" />
        </label>
        <img
          :src="resolveImage(item.product_detail?.image)"
          class="thumb"
          @click="router.push(`/product/${item.product_detail?.product_id}`)"
        />
        <div class="info">
          <div class="name">{{ item.product_detail?.name }}</div>
          <div class="price">¥{{ item.product_detail?.price }}</div>
          <div class="tags">
            <span v-if="item.category" class="tag" @click="editCategory(item)">{{ item.category }} ✎</span>
            <span v-else class="tag tag--add" @click="editCategory(item)">＋ 分类</span>
          </div>
        </div>
        <button class="remove" @click="removeOne(item.favorite_id)">✕</button>
      </article>
    </main>

    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">还没有收藏，去首页逛逛吧</div>
  </div>
</template>

<style scoped>
.favs {
  max-width: 640px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 16px;
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
  font-size: 18px;
  font-weight: 700;
}

.batch {
  padding: 6px 14px;
  border: none;
  border-radius: 999px;
  background: var(--hyc-cinnabar);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
}

.placeholder {
  width: 40px;
}

.filters {
  display: flex;
  gap: 8px;
  padding: 0 20px 14px;
  overflow-x: auto;
}

.chip {
  padding: 5px 14px;
  border: 1px solid #e5dccb;
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s var(--hyc-ease);
}

.chip.active {
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
  align-items: center;
  gap: 12px;
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 12px;
}

.check input {
  width: 18px;
  height: 18px;
  accent-color: var(--hyc-amber);
}

.thumb {
  width: 64px;
  height: 64px;
  border-radius: var(--hyc-radius-sm);
  object-fit: cover;
  cursor: pointer;
}

.info {
  flex: 1;
  min-width: 0;
}

.name {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.price {
  margin-top: 4px;
  color: var(--hyc-cinnabar);
  font-size: 15px;
  font-weight: 700;
}

.tags {
  margin-top: 6px;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  background: var(--hyc-amber-soft);
  color: var(--hyc-amber);
  border-radius: 999px;
  font-size: 11px;
  cursor: pointer;
}

.tag--add {
  background: transparent;
  border: 1px dashed #d5c8ae;
  color: var(--hyc-stone);
}

.remove {
  border: none;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 16px;
  cursor: pointer;
  padding: 4px;
}

.remove:hover {
  color: var(--hyc-cinnabar);
}

.state {
  padding: 80px 0;
  text-align: center;
  color: var(--hyc-stone);
}
</style>
