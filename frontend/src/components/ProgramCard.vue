<template>
  <article class="card" @click="goToProgram">
    <div class="header">
      <span class="format">{{ formatLabel }}</span>
      <button
        class="fav"
        @click.stop="emit('toggle-favorite', program.id)"
        :aria-label="isFavorite ? 'Убрать из избранного' : 'В избранное'"
      >
        {{ isFavorite ? '★' : '☆' }}
      </button>
    </div>

    <h3 class="title">{{ program.title }}</h3>

    <p class="center">
      {{ program.center?.name }}
    </p>

    <p class="description">
      {{ program.short_description || 'Описание отсутствует' }}
    </p>

    <div class="footer">
      <span class="price">
        {{ program.price ? `${program.price} KGS` : 'Цена по запросу' }}
      </span>
    </div>
  </article>
</template>


<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface Program {
  id: number
  title: string
  short_description?: string
  price?: number
  format?: 'ONLINE' | 'OFFLINE' | 'MIXED'
  center?: {
    name: string
  }
}

const props = defineProps<{
  program: Program
  favorites?: number[]
}>()

const emit = defineEmits<{
  (e: 'toggle-favorite', id: number): void
}>()

const isFavorite = computed(() =>
  props.favorites?.includes(props.program.id)
)

const formatLabel = computed(() => {
  switch (props.program.format) {
    case 'ONLINE': return 'Онлайн'
    case 'OFFLINE': return 'Оффлайн'
    case 'MIXED': return 'Смешанный'
    default: return ''
  }
})

function goToProgram() {
  router.push(`/programs/${props.program.id}`)
}
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.format {
  font-size: 12px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #4f7cff, #1a5cff);
  color: #fff;
}

.fav {
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #ffb400;
}

.title {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.35;
  color: #111;
}

.center {
  font-size: 13px;
  color: #6b7280;
}

.description {
  font-size: 14px;
  color: #374151;
  line-height: 1.45;
  flex-grow: 1;
}

.footer {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}

.price {
  font-size: 15px;
  font-weight: 600;
  color: #1a5cff;
}
</style>
