<template>
  <section v-if="program" class="page">
    <!-- Header -->
    <header class="hero">
      <div class="hero__top">
        <span v-if="formatLabel" class="badge badge--primary">{{ formatLabel }}</span>
        <span v-if="program.is_active === false" class="badge badge--muted">Неактивна</span>

        <div class="spacer" />
      </div>

      <h1 class="title">{{ program.title || 'Без названия' }}</h1>

      <p
        v-if="program.center?.description"
        class="center-description"
      >
        {{ program.center.description }}
      </p>

      <p v-if="program.center?.name" class="subtitle">
        {{ program.center.name }}
        <span v-if="program.center?.city" class="subtitle__sep">•</span>
        <span v-if="program.center?.city">{{ program.center.city }}</span>
      </p>

      <!-- Quick stats -->
      <div class="quick">
        <div class="quick__item" v-if="priceText">
          <span class="quick__label">Цена</span>
          <span class="quick__value">{{ priceText }}</span>
        </div>

        <div class="quick__item" v-if="program.duration || program.duration_hours || program.duration_weeks">
          <span class="quick__label">Длительность</span>
          <span class="quick__value">{{ durationText }}</span>
        </div>

        <div class="quick__item" v-if="program.rating_avg != null">
          <span class="quick__label">Рейтинг</span>
          <span class="quick__value">{{ Number(program.rating_avg).toFixed(1) }} ★</span>
        </div>

        <div class="quick__item" v-if="program.created_at">
          <span class="quick__label">Добавлено</span>
          <span class="quick__value">{{ formatDate(program.created_at) }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="actions">
        <a v-if="program.url" class="btn btn--primary" :href="program.url" target="_blank" rel="noopener">
          Перейти на страницу программы
        </a>

        <a
          v-if="program.center?.website"
          class="btn btn--ghost"
          :href="program.center.website"
          target="_blank"
          rel="noopener"
        >
          Сайт центра
        </a>

        <a v-if="program.center?.phone" class="btn btn--ghost" :href="`tel:${program.center.phone}`">
          Позвонить
        </a>
      </div>
    </header>

    <!-- Content grid -->
    <div class="grid">
      <!-- Main -->
      <main class="card">
        <h2 class="card__title">Описание</h2>
        <p class="text" v-if="program.description">{{ program.description }}</p>
        <p class="text text--muted" v-else>Подробное описание отсутствует</p>

        <div class="divider" />

        <h2 class="card__title">Характеристики</h2>

        <div class="kv">
          <div class="kv__row" v-if="program.category">
            <div class="kv__key">Категория</div>
            <div class="kv__val">
              <span v-if="typeof program.category === 'object'">
                {{ program.category.name || program.category.title || program.category.slug }}
              </span>
              <span v-else>{{ program.category }}</span>
            </div>
          </div>

          <div class="kv__row" v-if="program.topic">
            <div class="kv__key">Тема</div>
            <div class="kv__val">{{ program.topic }}</div>
          </div>

          <div class="kv__row" v-if="program.level">
            <div class="kv__key">Уровень</div>
            <div class="kv__val">{{ program.level }}</div>
          </div>

          <div class="kv__row" v-if="program.language">
            <div class="kv__key">Язык</div>
            <div class="kv__val">{{ program.language }}</div>
          </div>

          <div class="kv__row" v-if="program.format">
            <div class="kv__key">Формат</div>
            <div class="kv__val">{{ formatLabel }}</div>
          </div>

          <div class="kv__row" v-if="program.address || program.location">
            <div class="kv__key">Адрес</div>
            <div class="kv__val">{{ program.address || program.location }}</div>
          </div>

          <div class="kv__row" v-if="program.start_date">
            <div class="kv__key">Старт</div>
            <div class="kv__val">{{ formatDate(program.start_date) }}</div>
          </div>

          <div class="kv__row" v-if="program.end_date">
            <div class="kv__key">Окончание</div>
            <div class="kv__val">{{ formatDate(program.end_date) }}</div>
          </div>

          <div class="kv__row" v-if="program.updated_at">
            <div class="kv__key">Обновлено</div>
            <div class="kv__val">{{ formatDate(program.updated_at) }}</div>
          </div>

          <div class="kv__row" v-if="program.currency">
            <div class="kv__key">Валюта</div>
            <div class="kv__val">{{ program.currency }}</div>
          </div>

          <div class="kv__row" v-if="program.price != null">
            <div class="kv__key">Цена</div>
            <div class="kv__val">{{ priceText }}</div>
          </div>

          <div class="kv__row" v-if="program.tags?.length">
            <div class="kv__key">Теги</div>
            <div class="kv__val">
              <div class="chips">
                <span class="chip" v-for="(t, i) in program.tags" :key="i">{{ t }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="divider" />
      </main>

      <!-- Aside -->
      <aside class="stack">
        <section class="card">
          <h2 class="card__title">Учебный центр</h2>

          <div class="kv">
            <div class="kv__row" v-if="program.center?.name">
              <div class="kv__key">Название</div>
              <div class="kv__val">{{ program.center.name }}</div>
            </div>

            <div class="kv__row" v-if="program.center?.city">
              <div class="kv__key">Город</div>
              <div class="kv__val">{{ program.center.city }}</div>
            </div>

            <div class="kv__row" v-if="program.center?.address">
              <div class="kv__key">Адрес</div>
              <div class="kv__val">{{ program.center.address }}</div>
            </div>

            <div class="kv__row" v-if="program.center?.phone">
              <div class="kv__key">Телефон</div>
              <div class="kv__val">
                <a class="link" :href="`tel:${program.center.phone}`">{{ program.center.phone }}</a>
              </div>
            </div>

            <div class="kv__row" v-if="program.center?.email">
              <div class="kv__key">Email</div>
              <div class="kv__val">
                {{ program.center.email }}
              </div>
            </div>


            <div class="kv__row" v-if="program.center?.website">
              <div class="kv__key">Сайт</div>
              <div class="kv__val">
                <a class="link" :href="program.center.website" target="_blank" rel="noopener">
                  {{ program.center.website }}
                </a>
              </div>
            </div>
          </div>
        </section>

        <section class="card" v-if="contactsBlock">
          <h2 class="card__title">Контакты</h2>
          <div class="kv">
            <div class="kv__row" v-if="program.contact_name">
              <div class="kv__key">Контакт</div>
              <div class="kv__val">{{ program.contact_name }}</div>
            </div>
            <div class="kv__row" v-if="program.contact_phone">
              <div class="kv__key">Телефон</div>
              <div class="kv__val">
                <a class="link" :href="`tel:${program.contact_phone}`">{{ program.contact_phone }}</a>
              </div>
            </div>
            <div class="kv__row" v-if="program.contact_email">
              <div class="kv__key">Email</div>
              <div class="kv__val">
                {{ program.contact_email }}
              </div>
            </div>
          </div>
        </section>
      </aside>
    </div>
  </section>

  <div v-else class="loading">
    <div class="spinner" />
    <div>Загрузка…</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

type ProgramAny = Record<string, any>

const route = useRoute()
const program = ref<ProgramAny | null>(null)

onMounted(async () => {
  const { data } = await api.get(`/programs/${route.params.id}/`)
  program.value = data
})

const formatLabel = computed(() => {
  switch (program.value?.format) {
    case 'ONLINE': return 'Онлайн'
    case 'OFFLINE': return 'Оффлайн'
    case 'MIXED': return 'Смешанный'
    default: return ''
  }
})

const priceText = computed(() => {
  if (!program.value) return ''
  const cur = program.value.currency || 'KGS'
  const p = program.value.price

  if (p == null || p === '') return ''
  return `${p} ${cur}`
})

const durationText = computed(() => {
  const p = program.value
  if (!p) return ''
  if (p.duration) return String(p.duration)
  if (p.duration_hours) return `${p.duration_hours} часов`
  if (p.duration_weeks) return `${p.duration_weeks} недель`
  return ''
})

const contactsBlock = computed(() => {
  const p = program.value
  if (!p) return false
  return Boolean(p.contact_name || p.contact_phone || p.contact_email)
})

function formatDate(value: string) {
  // value может быть ISO: 2025-12-12T10:00:00Z или 2025-12-12
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: '2-digit' })
}
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 22px;
}

.hero {
  background: #fff;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 10px 30px rgba(0,0,0,.06);
  border: 1px solid rgba(17, 24, 39, 0.06);
}

.hero__top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.spacer { flex: 1; }

.meta {
  font-size: 12px;
  color: #6b7280;
}

.title {
  font-size: 28px;
  line-height: 1.15;
  margin: 0 0 10px;
  color: #111827;
  letter-spacing: -0.02em;
}
.center-description {
  margin-top: 8px;
  margin-bottom: 14px;
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  max-width: 820px;
}

.subtitle {
  margin: 0 0 16px;
  color: #6b7280;
  font-size: 14px;
}

.subtitle__sep {
  margin: 0 6px;
  opacity: .8;
}

.badge {
  font-size: 12px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  user-select: none;
}

.badge--primary {
  color: #fff;
  background: linear-gradient(135deg, #4f7cff, #1a5cff);
}

.badge--muted {
  color: #374151;
  background: #f3f4f6;
}

.quick {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.quick__item {
  padding: 12px;
  border-radius: 14px;
  background: #f9fafb;
  border: 1px solid rgba(17, 24, 39, 0.06);
}

.quick__label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 6px;
}

.quick__value {
  font-weight: 700;
  color: #111827;
  font-size: 14px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}

.btn {
  border-radius: 12px;
  padding: 10px 12px;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  border: 1px solid rgba(17, 24, 39, 0.10);
  color: #111827;
  background: #fff;
  transition: transform .15s ease, box-shadow .15s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(0,0,0,.08);
}

.btn--primary {
  border: none;
  color: #fff;
  background: linear-gradient(135deg, #4f7cff, #1a5cff);
}

.btn--ghost {
  background: #fff;
}

.grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1.6fr 0.9fr;
  gap: 16px;
}

.card {
  background: #fff;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,.05);
  border: 1px solid rgba(17, 24, 39, 0.06);
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card__title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 800;
  color: #111827;
}

.text {
  font-size: 15px;
  line-height: 1.65;
  color: #111827;
}

.text--muted {
  color: #6b7280;
}

.divider {
  height: 1px;
  background: rgba(17, 24, 39, 0.08);
  margin: 16px 0;
}

.kv {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.kv__row {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 12px;
  align-items: start;
}

.kv__key {
  font-size: 13px;
  color: #6b7280;
}

.kv__val {
  font-size: 14px;
  color: #111827;
  word-break: break-word;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid rgba(17, 24, 39, 0.06);
}

.link {
  color: #1a5cff;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.raw summary {
  cursor: pointer;
  font-weight: 700;
  color: #111827;
}

.raw pre {
  margin-top: 12px;
  padding: 12px;
  border-radius: 12px;
  background: #0b1220;
  color: #e5e7eb;
  font-size: 12px;
  line-height: 1.55;
  overflow: auto;
}

.loading {
  min-height: 55vh;
  display: grid;
  place-items: center;
  gap: 10px;
  color: #6b7280;
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
  .quick { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid { grid-template-columns: 1fr; }
  .kv__row { grid-template-columns: 1fr; gap: 4px; }
  .kv__key { font-size: 12px; }
}
</style>
