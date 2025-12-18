<template>
  <section class="page">
    <header class="top">
      <div>
        <h1 class="title">Учебные центры</h1>
      </div>

      <div class="controls">
        <label class="field">
          <span class="label">Поиск</span>
          <input
            v-model="search"
            class="input"
            type="text"
            placeholder="Введите данные искомого центра"
          />
        </label>

        <label class="field">
          <span class="label">Сортировка</span>
          <select v-model="ordering" class="select">
            <option value="name">Название (А–Я)</option>
            <option value="-name">Название (Я–А)</option>
            <option value="-created_at">Сначала новые</option>
            <option value="created_at">Сначала старые</option>
          </select>
        </label>
      </div>
    </header>

    <div v-if="loading" class="state">
      <div class="spinner" />
      <div>Загрузка…</div>
    </div>

    <div v-else-if="error" class="state state--error">
      <div class="error-title">Не удалось загрузить центры</div>
      <div class="error-text">{{ error }}</div>
      <button class="btn" @click="fetchCenters">Повторить</button>
    </div>

    <div v-else>
      <div class="meta-row">
        <div class="meta">
          Найдено: <b>{{ centers.length }}</b>
        </div>

        <button v-if="search" class="btn btn--ghost" @click="clearSearch">
          Сбросить поиск
        </button>
      </div>

      <div v-if="centers.length === 0" class="empty">
        Ничего не найдено.
      </div>

      <div v-else class="grid">
        <CenterCard
          v-for="c in centers"
          :key="c.id"
          :center="c"
          @open="goToCenter"
        />

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import CenterCard from '@/components/CenterCard.vue'

type Center = {
  id: number
  name: string
  city?: string
  address?: string
  phone?: string
  email?: string
  website?: string
  description?: string
  created_at?: string
}

const router = useRouter()

const centers = ref<Center[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const search = ref('')
const ordering = ref<'name' | '-name' | 'created_at' | '-created_at'>('name')

function buildParams() {
  // DRF SearchFilter + OrderingFilter
  const params: Record<string, any> = {
    ordering: ordering.value,
  }
  if (search.value.trim()) params.search = search.value.trim()
  return params
}

async function fetchCenters() {
  loading.value = true
  error.value = null

  try {
    const { data } = await api.get('/centers/', { params: buildParams() })
    // DRF может вернуть либо массив, либо пагинацию { results: [] }
    centers.value = Array.isArray(data) ? data : (data?.results ?? [])
  } catch (e: any) {
    error.value =
      e?.response?.data?.detail ||
      e?.message ||
      'Неизвестная ошибка'
  } finally {
    loading.value = false
  }
}

function clearSearch() {
  search.value = ''
}

function goToCenter(id: number) {
  router.push(`/centers/${id}`)
}

function formatDate(value: string) {
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleDateString('ru-RU', { year: 'numeric', month: 'short', day: '2-digit' })
}

// Debounce на поиск, чтобы не стрелять запросом на каждый символ
let t: number | null = null
watch([search, ordering], () => {
  if (t) window.clearTimeout(t)
  t = window.setTimeout(() => {
    fetchCenters()
  }, 350)
})

onMounted(() => {
  fetchCenters()
})
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 22px;
}

.top {
  background: #fff;
  border-radius: 18px;
  padding: 18px;
  border: 1px solid rgba(17, 24, 39, 0.06);
  box-shadow: 0 10px 30px rgba(0,0,0,.05);
}

.title {
  margin: 0 0 6px;
  font-size: 26px;
  color: #111827;
  letter-spacing: -0.02em;
}

.subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.controls {
  margin-top: 14px;
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 12px;
  color: #6b7280;
}

.select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;

  border-radius: 14px;
  padding: 10px 40px 10px 14px;
  border: 1px solid rgba(17, 24, 39, 0.12);
  background-color: #fff;
  background-image:
    linear-gradient(45deg, transparent 50%, #6b7280 50%),
    linear-gradient(135deg, #6b7280 50%, transparent 50%);
  background-position:
    calc(100% - 18px) calc(50% - 3px),
    calc(100% - 13px) calc(50% - 3px);
  background-size: 6px 6px;
  background-repeat: no-repeat;

  font-size: 14px;
  font-weight: 500;
  color: #111827;
  cursor: pointer;
  transition: border-color .15s ease, box-shadow .15s ease;
}

.select:hover {
  border-color: rgba(26, 92, 255, 0.35);
}

.select:focus {
  outline: none;
  border-color: rgba(26, 92, 255, 0.55);
  box-shadow: 0 0 0 4px rgba(26, 92, 255, 0.12);
}

/* Опции внутри списка */
.select option {
  font-size: 14px;
  padding: 10px;
}

.input {
  color: #111827;          /* чёрный / почти чёрный */
  background-color: #fff;
}

/* placeholder оставляем светлым */
.input::placeholder {
  color: #9ca3af;
  opacity: 1;              /* важно, чтобы не бледнел сильнее */
}

/* при фокусе текст тоже чёрный */
.input:focus {
  color: #111827;
}


.meta-row {
  margin-top: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta {
  color: #374151;
  font-size: 14px;
}

.grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.card {
  background: #fff;
  border-radius: 18px;
  padding: 16px;
  border: 1px solid rgba(17, 24, 39, 0.06);
  box-shadow: 0 10px 26px rgba(0,0,0,.05);
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 34px rgba(0,0,0,.10);
}

.card__head {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 10px;
}

.card__title {
  margin: 0;
  font-size: 16px;
  line-height: 1.35;
  color: #111827;
}

.pill {
  font-size: 12px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #374151;
  white-space: nowrap;
}

.card__line {
  margin: 0;
  font-size: 13px;
  color: #111827;
}

.card__desc {
  margin: 4px 0 0;
  font-size: 13px;
  line-height: 1.55;
  color: #4b5563;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

.card__foot {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid rgba(17, 24, 39, 0.08);
}

.muted {
  color: #6b7280;
}

.linkish {
  color: #1a5cff;
  font-weight: 700;
  font-size: 13px;
}

.state {
  min-height: 55vh;
  display: grid;
  place-items: center;
  gap: 10px;
  color: #6b7280;
}

.state--error {
  color: #991b1b;
}

.error-title {
  font-weight: 800;
  color: #111827;
}

.error-text {
  color: #6b7280;
  max-width: 520px;
  text-align: center;
}

.btn {
  border-radius: 12px;
  padding: 10px 12px;
  font-weight: 700;
  font-size: 14px;
  border: 1px solid rgba(17, 24, 39, 0.10);
  background: #fff;
  cursor: pointer;
}

.btn--ghost {
  background: #fff;
  color: #111827;
}

.empty {
  margin-top: 16px;
  color: #6b7280;
  padding: 18px;
  background: #fff;
  border: 1px solid rgba(17, 24, 39, 0.06);
  border-radius: 18px;
}

.spinner {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  border: 3px solid rgba(17, 24, 39, 0.15);
  border-top-color: rgba(17, 24, 39, 0.60);
  animation: spin .9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 980px) {
  .controls {
    grid-template-columns: 1fr;
  }
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
