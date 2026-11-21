<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { createClient } from '@hyc/request'

const client = createClient({ tokenKey: 'sjlocaltoken' })
const shops = ref<any[]>([])
const form = ref({ name: '', phone_number: '', password: '', password_confirm: '', shop: '' as number | '' })

async function loadShops() {
  try {
    const res = await client.get('/api/shops/', { params: { page_size: 50 } })
    shops.value = res.data.results || []
    if (shops.value.length) form.value.shop = shops.value[0].shop_id
  } catch (e) {
    console.error(e)
  }
}

async function submit() {
  try {
    await client.post('/api/merchants/staffs/', form.value)
    alert('员工添加成功')
    form.value = { name: '', phone_number: '', password: '', password_confirm: '', shop: shops.value[0]?.shop_id || '' }
  } catch (e: any) {
    alert(Object.values(e.response?.data || {}).flat().join('；') || '添加失败')
  }
}

onMounted(loadShops)
</script>

<template>
  <div class="staffs">
    <header class="head">
      <h1 class="title">员工管理</h1>
    </header>

    <form class="form" @submit.prevent="submit">
      <label class="field">
        <span>归属店铺</span>
        <select v-model="form.shop" required>
          <option v-for="s in shops" :key="s.shop_id" :value="s.shop_id">{{ s.name }}</option>
        </select>
      </label>
      <label class="field">
        <span>员工姓名</span>
        <input v-model="form.name" type="text" placeholder="请输入姓名" required />
      </label>
      <label class="field">
        <span>手机号</span>
        <input v-model="form.phone_number" type="tel" placeholder="11 位手机号" required />
      </label>
      <label class="field">
        <span>密码</span>
        <input v-model="form.password" type="password" placeholder="至少 6 位" required />
      </label>
      <label class="field">
        <span>确认密码</span>
        <input v-model="form.password_confirm" type="password" placeholder="再次输入" required />
      </label>
      <button class="submit" type="submit">添加员工</button>
    </form>
  </div>
</template>

<style scoped>
.staffs {
  max-width: 480px;
}

.head {
  margin-bottom: 20px;
}

.title {
  font-family: var(--hyc-font-display);
  font-size: 22px;
}

.form {
  background: var(--hyc-paper);
  border-radius: var(--hyc-radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
}

.field input,
.field select {
  padding: 11px 14px;
  border: 1px solid #e5dccb;
  border-radius: var(--hyc-radius-sm);
  background: #fffdf8;
  font-size: 14px;
  outline: none;
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
</style>
