<template>
  <section class="page">
    <div v-if="loading" class="state">Загрузка…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <div v-else-if="center">
      <header class="hero">
        <h1 class="title">{{ center.name }}</h1>

        <p class="subtitle" v-if="center.city || center.address">
          <span v-if="center.city">{{ center.city }}</span>
          <span v-if="center.city && center.address"> • </span>
          <span v-if="center.address">{{ center.address }}</span>
        </p>

        <p v-if="center.description" class="description">
          {{ center.description }}
        </p>

        <div class="actions">
          <a v-if="center.website" :href="center.website" target="_blank" class="btn primary">
            Сайт центра
          </a>
          <button class="btn" @click="goBack">Назад</button>
        </div>
      </header>

      <div class="card">
        <div class="row" v-if="center.phone">
          <span class="key">Телефон</span>
          <span>{{ center.phone }}</span>
        </div>

        <div class="row" v-if="center.email">
          <span class="key">Email</span>
          <span>{{ center.email }}</span>
        </div>

        <div class="row" v-if="center.created_at">
          <span class="key">Создан</span>
          <span>{{ formatDate(center.created_at) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()

const center = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchCenter() {
  loading.value = true
  try {
    const { data } = await api.get(`/centers/${route.params.id}/`)
    center.value = data
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}

function formatDate(value: string) {
  const d = new Date(value)
  return d.toLocaleDateString('ru-RU')
}

onMounted(fetchCenter)
</script>

<style scoped>
.page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}
.hero {
  background: #fff;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 10px 30px rgba(0,0,0,.06);
}
.title {
  font-size: 28px;
  font-weight: 800;
}
.subtitle {
  color: #6b7280;
  margin: 8px 0 12px;
}
.description {
  line-height: 1.6;
  color: #374151;
}
.actions {
  margin-top: 16px;
  display: flex;
  gap: 10px;
}
.btn {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(17,24,39,.1);
  background: #fff;
  cursor: pointer;
}
.primary {
  background: linear-gradient(135deg,#4f7cff,#1a5cff);
  color: #fff;
  border: none;
}
.card {
  margin-top: 16px;
  background: #fff;
  border-radius: 18px;
  padding: 18px;
}
.row {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}
.key {
  width: 120px;
  color: #6b7280;
}
.state {
  text-align: center;
  padding: 40px;
}
.error {
  color: #991b1b;
}
</style>
