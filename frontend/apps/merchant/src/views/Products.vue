<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { createClient } from '@hyc/request'

const client = createClient({ tokenKey: 'sjlocaltoken' })
const shops = ref<any[]>([])
const currentShopId = ref<number | ''>('')
const products = ref<any[]>([])
const loading = ref(true)
const showForm = ref(false)
const currentPage = ref(1)
const totalCount = ref(0)

const form = ref({
  shop_id: '' as number | '',
  name: '',
  description: '',
  price: '',
  category: '其他',
  is_active: true,
  image: '',
})

const categories = ['食品', '服装', '电子产品', '家居用品', '其他']

async function loadShops() {
  const res = await client.get('/api/shops/', { params: { page_size: 50 } })
  shops.value = res.data.results || []
  if (shops.value.length) {
    currentShopId.value = shops.value[0].shop_id
    form.value.shop_id = shops.value[0].shop_id
    loadProducts()
  }
}

async function loadProducts(page = 1) {
  if (currentShopId.value === '') return
  loading.value = true
  try {
    const res = await client.get('/api/products/', {
      params: { shop_id: currentShopId.value, page },
    })
    products.value = res.data.results || []
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
  if (currentPage.value > 1) loadProducts(currentPage.value - 1)
}

function nextPage() {
  if (currentPage.value < totalPages.value) loadProducts(currentPage.value + 1)
}

function onShopChange() {
  form.value.shop_id = currentShopId.value
  loadProducts()
}

async function submit() {
  try {
    const data: any = { ...form.value, price: parseFloat(form.value.price) }
    if (data.image) data.image = [data.image]
    else delete data.image
    await client.post('/api/products/', data)
    alert('商品添加成功')
    showForm.value = false
    loadProducts()
  } catch (e: any) {
    alert(Object.values(e.response?.data || {}).flat().join('；') || '添加失败')
  }
}

async function remove(id: number) {
  if (!confirm('确定删除该商品吗？')) return
  try {
    await client.delete(`/api/products/${id}/`)
    loadProducts()
  } catch (e) {
    console.error(e)
  }
}

async function toggleActive(p: any) {
  try {
    await client.patch(`/api/products/${p.product_id}/`, { is_active: !p.is_active })
    p.is_active = !p.is_active
  } catch (e) {
    console.error(e)
  }
}

async function aiCopywriting() {
  if (!form.value.name) {
    alert('请先填写商品名称')
    return
  }
  try {
    const res = await client.post('/api/ai/copywriting/', {
      name: form.value.name,
      category: form.value.category,
      selling_points: form.value.description || '品质好物，值得信赖',
    })
    form.value.description = res.data.description
    alert('AI 文案已生成并填入描述')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'AI 文案生成失败')
  }
}

onMounted(loadShops)
</script>

<template>
  <div class="products">
    <header class="head">
      <h1 class="title">商品管理</h1>
      <button class="btn" @click="showForm = !showForm">{{ showForm ? '取消' : '＋ 添加商品' }}</button>
    </header>

    <div v-if="shops.length" class="shopbar">
      <span class="label">当前店铺：</span>
      <select v-model="currentShopId" @change="onShopChange">
        <option v-for="s in shops" :key="s.shop_id" :value="s.shop_id">{{ s.name }}</option>
      </select>
    </div>

    <form v-if="showForm" class="form" @submit.prevent="submit">
      <input v-model="form.name" type="text" placeholder="商品名称" required />
      <textarea v-model="form.description" rows="2" placeholder="商品描述（可选）"></textarea>
      <button type="button" class="ai-btn" @click="aiCopywriting">✨ AI 生成文案</button>
      <div class="row2">
        <input v-model="form.price" type="number" step="0.01" min="0" placeholder="价格" required />
        <select v-model="form.category">
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <label class="check">
        <input v-model="form.is_active" type="checkbox" /> 立即上架
      </label>
      <input v-model="form.image" type="text" placeholder="商品图片 URL（可选）" />
      <button class="submit" type="submit">保存商品</button>
    </form>

    <main v-if="products.length" class="list">
      <article v-for="p in products" :key="p.product_id" class="row">
        <div class="info">
          <div class="name">{{ p.name }}</div>
          <div class="meta">{{ p.category }} · ¥{{ p.price }}</div>
        </div>
        <button class="toggle" :class="{ on: p.is_active }" @click="toggleActive(p)">
          {{ p.is_active ? '上架' : '下架' }}
        </button>
        <button class="del" @click="remove(p.product_id)">删除</button>
      </article>
    </main>

    <div v-if="totalPages > 1" class="pager">
      <button class="pager-btn" :disabled="currentPage <= 1" @click="prevPage">上一页</button>
      <span class="pager-info">{{ currentPage }} / {{ totalPages }} · 共 {{ totalCount }} 条</span>
      <button class="pager-btn" :disabled="currentPage >= totalPages" @click="nextPage">下一页</button>
    </div>

    <div v-else-if="loading" class="state">加载中…</div>
    <div v-else class="state">暂无商品</div>
  </div>
</template>

<style scoped>
.products {
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

.shopbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-size: 14px;
}

.shopbar select {
  padding: 8px 12px;
  border: 1px solid #e5dccb;
  border-radius: var(--hyc-radius-sm);
  background: #fffdf8;
  font-size: 14px;
  outline: none;
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
.form textarea,
.form select {
  padding: 11px 14px;
  border: 1px solid #e5dccb;
  border-radius: var(--hyc-radius-sm);
  background: #fffdf8;
  font-size: 14px;
  outline: none;
  font-family: inherit;
}

.row2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.check {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
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

.ai-btn {
  padding: 10px;
  border: 1px dashed var(--hyc-amber);
  border-radius: var(--hyc-radius-sm);
  background: transparent;
  color: var(--hyc-amber);
  font-size: 13px;
  cursor: pointer;
}

.list {
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
  padding: 6px 14px;
  border: 1px solid #d5c8ae;
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-stone);
  font-size: 13px;
  cursor: pointer;
}

.toggle.on {
  border-color: var(--hyc-amber);
  color: var(--hyc-amber);
}

.del {
  padding: 6px 14px;
  border: none;
  border-radius: 999px;
  background: transparent;
  color: var(--hyc-cinnabar);
  font-size: 13px;
  cursor: pointer;
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
