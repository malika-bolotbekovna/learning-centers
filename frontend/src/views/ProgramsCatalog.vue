<!-- src/views/ProgramsCatalog.vue -->
<template>
  <section class="container">
    <h1>Каталог программ</h1>

    <!-- Фильтры -->
    <div class="controls">
      <input
        v-model="catalog.q"
        placeholder="Поиск по названию, теме, городу"
        @input="onFiltersChange"
      />

      <select v-model="catalog.filters.program_format" @change="onFiltersChange">
        <option value="">Формат: любой</option>
        <option value="ONLINE">Онлайн</option>
        <option value="OFFLINE">Оффлайн</option>
        <option value="MIXED">Смешанный</option>
      </select>

      <!-- ✅ Фильтр по категории -->
      <select v-model="catalog.filters.category" @change="onFiltersChange" :disabled="categoriesLoading">
        <option value="">
          {{ categoriesLoading ? 'Категории: загрузка…' : 'Категория: любая' }}
        </option>
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
    </div>

    <div v-if="categoriesError" class="cat-error">
      {{ categoriesError }}
    </div>

    <!-- Загрузка -->
    <div v-if="catalog.loading" class="loading">
      Загрузка…
    </div>

    <!-- Список программ -->
    <div v-else class="grid">
      <ProgramCard
        v-for="p in catalog.programs"
        :key="p.id"
        :program="p"
        :favorites="favorites.ids"
        @toggle-favorite="onToggleFavorite"
      />
    </div>

    <!-- Modal: требуется авторизация -->
    <div v-if="showAuthModal" class="modalOverlay" @click.self="showAuthModal = false">
      <div class="modal">
        <h3 class="modalTitle">Нужно войти</h3>
        <p class="modalText">
          Чтобы добавлять программы в избранное, войдите или зарегистрируйтесь.
        </p>

        <div class="modalActions">
          <button class="btn" @click="showAuthModal = false">Закрыть</button>
          <button class="btn primary" @click="goLogin">Войти</button>
          <button class="btn ghost" @click="goRegister">Регистрация</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useCatalog } from '@/stores/catalog'
import { useFavorites } from '@/stores/favorites'
import { useAuth } from '@/stores/auth'
import ProgramCard from '@/components/ProgramCard.vue'

type Category = { id: number; name: string; slug?: string }

const router = useRouter()
const catalog = useCatalog()
const favorites = useFavorites()
const auth = useAuth()

const showAuthModal = ref(false)
const isAuth = computed(() => !!auth.user)

/** ✅ Категории для фильтра */
const categories = ref<Category[]>([])
const categoriesLoading = ref(false)
const categoriesError = ref<string | null>(null)

async function loadCategories() {
  categoriesLoading.value = true
  categoriesError.value = null
  try {
    const { data } = await api.get('/categories/')
    categories.value = Array.isArray(data) ? data : (data?.results ?? [])
  } catch (e: any) {
    categoriesError.value = e?.response?.data?.detail || 'Не удалось загрузить категории'
    categories.value = []
  } finally {
    categoriesLoading.value = false
  }
}

async function onToggleFavorite(programId: number) {
  if (!isAuth.value) {
    showAuthModal.value = true
    return
  }
  await favorites.toggle(programId)
}

function onFiltersChange() {
  catalog.page = 1
  catalog.load()
}

function goLogin() {
  showAuthModal.value = false
  router.push('/login')
}

function goRegister() {
  showAuthModal.value = false
  router.push('/register')
}

onMounted(async () => {
  // ✅ подгружаем категории для фильтра
  await loadCategories()

  // первая загрузка каталога
  if (!catalog.programs.length) {
    await catalog.load()
  }

  // избранное грузим только если авторизован
  if (isAuth.value) {
    await favorites.load()
  }
})
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 16px 0;
}

.controls input,
.controls select {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid rgba(17, 24, 39, 0.14);
  font-size: 14px;
  background: #fff;
}

.cat-error {
  margin-top: -6px;
  margin-bottom: 10px;
  color: #b91c1c;
  font-weight: 700;
}

.loading {
  margin-top: 30px;
  text-align: center;
  font-size: 16px;
}

.grid {
  display: grid;
  gap: 20px;
  margin-top: 20px;

  /* 3 колонки на широких */
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

/* 2 колонки */
@media (max-width: 1100px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* 1 колонка */
@media (max-width: 720px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

/* ВАЖНО: запретить карточке растягиваться на всю строку */
.grid > * {
  min-width: 0;
  grid-column: auto !important;
}

/* ===== Modal ===== */
.modalOverlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 16px;
}

.modal {
  width: min(460px, 100%);
  background: #fff;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(17, 24, 39, 0.12);
}

.modalTitle {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 900;
  color: #111;
}

.modalText {
  margin: 0 0 14px;
  color: #111;
  opacity: 0.85;
  line-height: 1.5;
}

.modalActions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(17, 24, 39, 0.14);
  background: #fff;
  cursor: pointer;
  font-weight: 800;
  color: #111;
}

.primary {
  border: none;
  color: #fff;
  background: linear-gradient(135deg, #4f7cff, #1a5cff);
}

.ghost {
  background: #fff;
  border: 1px solid #4f7cff;
  color: #4f7cff;
  font-weight: 800;
}

.ghost:hover {
  background: rgba(79, 124, 255, 0.08);
}

.ghost:active {
  background: rgba(79, 124, 255, 0.16);
}
</style>
