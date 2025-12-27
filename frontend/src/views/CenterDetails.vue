<template>
  <section class="page">
    <div v-if="loading" class="state">Загрузка…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <div v-else-if="center">
      <header class="hero">
        <div class="heroTop">
          <div>
            <h1 class="title">{{ center.name }}</h1>

            <p class="subtitle" v-if="center.city || center.address">
              <span v-if="center.city">{{ center.city }}</span>
              <span v-if="center.city && center.address"> • </span>
              <span v-if="center.address">{{ center.address }}</span>
            </p>

            <p v-if="center.description" class="description">
              {{ center.description }}
            </p>
          </div>

          <div class="ratingBox">
            <div class="ratingValue">
              <span class="ratingNum">{{ formatAvg(center.rating_avg) }}</span>
              <span class="ratingMax">/ 5</span>
            </div>
            <div class="stars" aria-label="Рейтинг центра">
              <span
                v-for="n in 5"
                :key="n"
                class="star"
                :class="{ on: n <= Math.round(Number(center.rating_avg || 0)) }"
              >
                ★
              </span>
            </div>
            <div class="ratingMeta">
              <span>{{ reviewsTotalLabel }}</span>
            </div>
          </div>
        </div>

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

      <!-- Reviews -->
      <section class="reviews">
        <div class="reviewsHeader">
          <h2 class="h2">Отзывы</h2>

          <div class="reviewsTools">
            <select class="select" v-model="sort">
              <option value="-created_at">Сначала новые</option>
              <option value="created_at">Сначала старые</option>
              <option value="-rating">Сначала высокий рейтинг</option>
              <option value="rating">Сначала низкий рейтинг</option>
            </select>

            <button class="btn" @click="fetchReviews" :disabled="reviewsLoading">
              Обновить
            </button>
          </div>
        </div>

        <div v-if="reviewsError" class="alert error">{{ reviewsError }}</div>

        <!-- Add review -->
        <div class="reviewFormCard">
          <div class="formTitle">Оставить отзыв</div>

          <div class="formGrid">
            <div class="field">
              <label class="label">Оценка</label>
              <div class="starsInput" role="radiogroup" aria-label="Выберите оценку">
                <button
                  v-for="n in 5"
                  :key="n"
                  type="button"
                  class="starBtn"
                  :class="{ on: n <= newReview.rating }"
                  @click="newReview.rating = n"
                >
                  ★
                </button>
              </div>
              <div class="hint">Выбрано: {{ newReview.rating }} / 5</div>
            </div>

            <div class="field">
              <label class="label">Текст</label>
              <textarea
                class="textarea"
                v-model.trim="newReview.text"
                rows="4"
                placeholder="Напишите, что понравилось и что можно улучшить"
              />
              <div class="hint">Минимум 5 символов</div>
            </div>
          </div>

          <div class="formActions">
            <button class="btn primary" @click="createReview" :disabled="createDisabled">
              {{ creating ? 'Отправка…' : 'Добавить отзыв' }}
            </button>
            <button class="btn" @click="resetForm" :disabled="creating">
              Очистить
            </button>
          </div>

          <div v-if="createError" class="alert error">{{ createError }}</div>
          <div v-if="createSuccess" class="alert success">{{ createSuccess }}</div>
        </div>

        <!-- List -->
        <div class="reviewList">
          <div v-if="reviewsLoading" class="state">Загрузка отзывов…</div>

          <div v-else-if="reviews.length === 0" class="empty">
            Пока нет отзывов. Будьте первым.
          </div>

          <article v-else v-for="r in reviews" :key="r.id" class="reviewItem">
            <div class="reviewTop">
              <div class="reviewAuthor">
                <div class="avatar">{{ initials(r.author_name || 'U') }}</div>
                <div>
                  <div class="authorName">{{ r.author_name || 'Пользователь' }}</div>
                  <div class="reviewDate">{{ formatDateTime(r.created_at) }}</div>
                </div>
              </div>

              <div class="reviewRating" :aria-label="`Оценка ${r.rating} из 5`">
                <span v-for="n in 5" :key="n" class="star" :class="{ on: n <= Number(r.rating || 0) }">★</span>
              </div>
            </div>

            <div class="reviewBody" v-if="editingId !== r.id">
              {{ r.text }}
            </div>

            <!-- Edit mode (если разрешено бэком) -->
            <div v-else class="editBox">
              <div class="field">
                <label class="label">Оценка</label>
                <div class="starsInput">
                  <button
                    v-for="n in 5"
                    :key="n"
                    type="button"
                    class="starBtn"
                    :class="{ on: n <= editModel.rating }"
                    @click="editModel.rating = n"
                  >
                    ★
                  </button>
                </div>
              </div>

              <div class="field">
                <label class="label">Текст</label>
                <textarea class="textarea" v-model.trim="editModel.text" rows="4" />
              </div>

              <div class="formActions">
                <button class="btn primary" @click="saveEdit(r.id)" :disabled="savingEdit">
                  {{ savingEdit ? 'Сохранение…' : 'Сохранить' }}
                </button>
                <button class="btn" @click="cancelEdit" :disabled="savingEdit">Отмена</button>
              </div>

              <div v-if="editError" class="alert error">{{ editError }}</div>
            </div>

            <div class="reviewActions">
              <button class="linkBtn" v-if="editingId !== r.id" @click="startEdit(r)">
                Редактировать
              </button>
              <button class="linkBtn danger" @click="deleteReview(r.id)" :disabled="deletingId === r.id">
                {{ deletingId === r.id ? 'Удаление…' : 'Удалить' }}
              </button>
            </div>
          </article>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

type Review = {
  id: number
  center: number
  author: number           // ID пользователя
  author_name: string      // имя автора
  rating: number
  text: string
  is_published: boolean
  created_at: string
}


const route = useRoute()
const router = useRouter()

const center = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const reviews = ref<Review[]>([])
const reviewsLoading = ref(false)
const reviewsError = ref<string | null>(null)

const sort = ref<string>('-created_at')

const newReview = reactive<{ rating: number; text: string }>({
  rating: 5,
  text: '',
})
const creating = ref(false)
const createError = ref<string | null>(null)
const createSuccess = ref<string | null>(null)

const editingId = ref<number | null>(null)
const editModel = reactive<{ rating: number; text: string }>({ rating: 5, text: '' })
const savingEdit = ref(false)
const editError = ref<string | null>(null)

const deletingId = ref<number | null>(null)

const centerId = computed(() => Number(route.params.id))

const createDisabled = computed(() => {
  if (creating.value) return true
  if (!centerId.value) return true
  if (!newReview.rating || newReview.rating < 1 || newReview.rating > 5) return true
  if (!newReview.text || newReview.text.length < 5) return true
  return false
})

const reviewsTotalLabel = computed(() => {
  const n = reviews.value.length
  if (n === 0) return 'Нет отзывов'
  if (n === 1) return '1 отзыв'
  if (n >= 2 && n <= 4) return `${n} отзыва`
  return `${n} отзывов`
})

async function fetchCenter() {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get(`/centers/${centerId.value}/`)
    center.value = data
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

async function fetchReviews() {
  reviewsLoading.value = true
  reviewsError.value = null
  try {
    // стандартный фильтр по center
    const { data } = await api.get(`/reviews/`, {
      params: { center: centerId.value, ordering: sort.value },
    })

    // если DRF pagination включена: { results: [...] }
    const list = Array.isArray(data) ? data : (data?.results ?? [])
    reviews.value = list
  } catch (e: any) {
    reviewsError.value = e?.response?.data?.detail || 'Ошибка загрузки отзывов'
  } finally {
    reviewsLoading.value = false
  }
}

async function createReview() {
  if (createDisabled.value) return
  creating.value = true
  createError.value = null
  createSuccess.value = null
  try {
    // поправь поля, если сериализатор ожидает другие названия
    await api.post(`/reviews/`, {
      center: centerId.value,
      rating: newReview.rating,
      text: newReview.text,
    })

    createSuccess.value = 'Отзыв отправлен'
    resetForm()
    await fetchReviews()
    // подтянем обновлённый рейтинг центра (так как ты обновляешь rating_avg на бэке)
    await fetchCenter()
  } catch (e: any) {
    // DRF часто отдаёт объект ошибок по полям
    const data = e?.response?.data
    createError.value =
      data?.detail ||
      data?.non_field_errors?.[0] ||
      data?.text?.[0] ||
      data?.rating?.[0] ||
      'Не удалось добавить отзыв'
  } finally {
    creating.value = false
  }
}

function resetForm() {
  newReview.rating = 5
  newReview.text = ''
}

function goBack() {
  router.back()
}

function formatDate(value: string) {
  const d = new Date(value)
  return d.toLocaleDateString('ru-RU')
}

function formatDateTime(value: string) {
  const d = new Date(value)
  return d.toLocaleString('ru-RU', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function formatAvg(v: any) {
  const n = Number(v || 0)
  return n.toFixed(1)
}

function initials(name: string) {
  const s = String(name || '').trim()
  if (!s) return 'U'
  return s.slice(0, 1).toUpperCase()
}

function startEdit(r: Review) {
  editingId.value = r.id
  editError.value = null
  editModel.rating = Number(r.rating || 5)
  editModel.text = r.text || ''
}

function cancelEdit() {
  editingId.value = null
  editError.value = null
}

async function saveEdit(id: number) {
  if (!editingId.value) return
  savingEdit.value = true
  editError.value = null
  try {
    await api.patch(`/reviews/${id}/`, {
      rating: editModel.rating,
      text: editModel.text,
    })
    editingId.value = null
    await fetchReviews()
    await fetchCenter()
  } catch (e: any) {
    const data = e?.response?.data
    editError.value =
      data?.detail ||
      data?.non_field_errors?.[0] ||
      data?.text?.[0] ||
      data?.rating?.[0] ||
      'Не удалось сохранить'
  } finally {
    savingEdit.value = false
  }
}

async function deleteReview(id: number) {
  deletingId.value = id
  try {
    await api.delete(`/reviews/${id}/`)
    await fetchReviews()
    await fetchCenter()
  } catch (e: any) {
    // если прав нет — будет 403
    reviewsError.value = e?.response?.data?.detail || 'Не удалось удалить отзыв'
  } finally {
    deletingId.value = null
  }
}

watch(sort, () => {
  fetchReviews()
})

onMounted(async () => {
  await fetchCenter()
  await fetchReviews()
})
</script>

<style scoped>
.page {
  max-width: 980px;
  margin: 0 auto;
  padding: 28px 18px 60px;
}

/* ===== HERO ===== */
.hero {
  background: rgba(255, 255, 255, 0.96);
  border-radius: 22px;
  padding: 26px;
  border: 1px solid rgba(17, 24, 39, 0.10);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
  backdrop-filter: blur(6px);
}

.title {
  font-size: 34px;
  line-height: 1.1;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: #0b0f19;
  margin: 0;
}

.subtitle {
  color: #0b0f19;
  opacity: 0.85;
  margin: 10px 0 12px;
  font-size: 15px;
}

.description {
  color: #0b0f19;
  opacity: 0.92;
  line-height: 1.7;
  font-size: 15px;
  margin-top: 10px;
  max-width: 720px;
}

.actions {
  margin-top: 18px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Buttons */
.btn {
  padding: 11px 14px;
  border-radius: 14px;
  border: 1px solid rgba(17, 24, 39, 0.14);
  background: #fff;
  cursor: pointer;
  font-weight: 700;
  color: #0b0f19;
  transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(0,0,0,.10);
}

.btn:active {
  transform: translateY(0);
  box-shadow: none;
}

.btn:disabled {
  opacity: .65;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.primary {
  border: none;
  color: #fff;
  background: linear-gradient(135deg, #4f7cff, #1a5cff);
}

/* ===== INFO CARD ===== */
.card {
  margin-top: 16px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 22px;
  padding: 18px 18px;
  border: 1px solid rgba(17, 24, 39, 0.10);
  box-shadow: 0 14px 38px rgba(0,0,0,.14);
}

.row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px;
  padding: 10px 8px;
  border-radius: 14px;
}

.row:not(:last-child) {
  border-bottom: 1px solid rgba(17, 24, 39, 0.08);
}

.key {
  color: #0b0f19;
  opacity: 0.72;
  font-weight: 700;
}

.row span:last-child {
  color: #0b0f19;
  font-weight: 600;
}

/* ===== STATES ===== */
.state {
  text-align: center;
  padding: 50px 12px;
  color: rgba(255,255,255,.85);
  font-weight: 700;
}

.error {
  color: #ffb4b4;
}

/* ===== REVIEWS SECTION ===== */
.reviews {
  margin-top: 22px;
}

.reviewsHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 18px 0 10px;
}

.h2 {
  font-size: 20px;
  font-weight: 900;
  letter-spacing: -0.01em;
  color: rgba(255,255,255,.92);
  margin: 0;
}

.reviewsTools {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* Select / input on dark bg */
.select {
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.08);
  color: rgba(255,255,255,.92);
  outline: none;
  font-weight: 700;
}

.select option {
  color: #0b0f19;
}

/* ===== FORM CARD ===== */
.reviewFormCard {
  background: rgba(255, 255, 255, 0.96);
  border-radius: 22px;
  padding: 18px;
  border: 1px solid rgba(17, 24, 39, 0.10);
  box-shadow: 0 18px 50px rgba(0,0,0,.18);
}

.formTitle {
  font-weight: 900;
  color: #0b0f19;
  margin-bottom: 12px;
  font-size: 16px;
}

.formGrid {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 12px;
  font-weight: 800;
  color: #0b0f19;
  opacity: 0.70;
}

.textarea {
  border: 1px solid rgba(17, 24, 39, 0.14);
  border-radius: 16px;
  padding: 12px 14px;
  outline: none;
  resize: vertical;
  font-family: inherit;
  color: #0b0f19;
  background: #fff;
  transition: box-shadow .12s ease, border-color .12s ease;
}

.textarea:focus {
  border-color: rgba(79,124,255,.55);
  box-shadow: 0 0 0 5px rgba(79,124,255,.16);
}

.hint {
  font-size: 12px;
  color: #0b0f19;
  opacity: 0.65;
  font-weight: 600;
}

/* Stars input */
.starsInput {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.starBtn {
  width: 42px;
  height: 38px;
  border-radius: 14px;
  border: 1px solid rgba(17,24,39,.14);
  background: #fff;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  color: rgba(17,24,39,.35);
  transition: transform .12s ease, box-shadow .12s ease, background .12s ease, color .12s ease;
}

.starBtn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(0,0,0,.10);
}

.starBtn.on {
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.35);
  background: rgba(245, 158, 11, 0.10);
}

.formActions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Alerts */
.alert {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
}

.alert.error {
  background: rgba(220, 38, 38, 0.10);
  border: 1px solid rgba(220, 38, 38, 0.22);
  color: #991b1b;
}

.alert.success {
  background: rgba(16, 185, 129, 0.10);
  border: 1px solid rgba(16, 185, 129, 0.22);
  color: #065f46;
}

/* ===== LIST ===== */
.reviewList {
  margin-top: 14px;
  display: grid;
  gap: 12px;
}

.reviewItem {
  background: rgba(255,255,255,.96);
  border-radius: 22px;
  padding: 16px;
  border: 1px solid rgba(17, 24, 39, 0.10);
  box-shadow: 0 18px 50px rgba(0,0,0,.16);
}

.reviewTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.reviewAuthor {
  display: flex;
  gap: 10px;
  align-items: center;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  font-weight: 900;
  background: rgba(79, 124, 255, 0.14);
  color: #1a5cff;
}

.authorName {
  font-weight: 900;
  color: #0b0f19;
}

.reviewDate {
  font-size: 12px;
  color: #0b0f19;
  opacity: 0.60;
  font-weight: 700;
}

.reviewRating .star {
  font-size: 16px;
  color: rgba(17,24,39,.18);
}
.reviewRating .star.on {
  color: #f59e0b;
}

.reviewBody {
  margin-top: 10px;
  color: #0b0f19;
  opacity: 0.90;
  line-height: 1.7;
  white-space: pre-wrap;
  font-weight: 600;
}

/* Edit/Delete */
.reviewActions {
  margin-top: 12px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.linkBtn {
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
  font-weight: 900;
  color: #1a5cff;
}

.linkBtn:hover {
  text-decoration: underline;
}

.linkBtn.danger {
  color: #b91c1c;
}

/* Empty */
.empty {
  text-align: center;
  color: rgba(255,255,255,.85);
  padding: 18px 8px;
  font-weight: 800;
}

/* ===== Responsive ===== */
@media (max-width: 760px) {
  .formGrid {
    grid-template-columns: 1fr;
  }

  .row {
    grid-template-columns: 1fr;
  }

  .title {
    font-size: 28px;
  }
}
/* ===== FIX RATING COLORS ===== */

/* число рейтинга */
.ratingNum,
.ratingMax {
  color: #000 !important;
  opacity: 1 !important;
}

/* текст "1 отзыв" */
.ratingMeta,
.ratingMeta span {
  color: #000 !important;
  opacity: 1 !important;
}

/* звезды */
.stars .star {
  color: #000 !important;
  opacity: 1 !important;
}

/* если есть выключенные звезды */
.stars .star.on {
  color: #f59e0b !important;
  opacity: 1 !important;
}

/* на всякий случай — если рейтинг в отдельной карточке */
.ratingBox * {
  color: #000;
  opacity: 1;
}

</style>
