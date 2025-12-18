<template>
  <article class="card" @click="$emit('open', center.id)">
    <div class="head">
      <h3 class="title">{{ center.name || 'Без названия' }}</h3>
      <span v-if="center.city" class="pill">{{ center.city }}</span>
    </div>

    <div class="body">
      <p v-if="center.address" class="line">
        <span class="label">Адрес:</span>
        <span class="value">{{ center.address }}</span>
      </p>

      <p v-if="center.phone" class="line">
        <span class="label">Телефон:</span>
        <span class="value">{{ center.phone }}</span>
      </p>

      <p v-if="center.email" class="line">
        <span class="label">Email:</span>
        <span class="value">{{ center.email }}</span>
      </p>

      <p v-if="center.description" class="desc">
        {{ center.description }}
      </p>
    </div>

    <div class="foot">
      <span class="date" v-if="center.created_at">{{ formatDate(center.created_at) }}</span>
      <span class="open">Открыть →</span>
    </div>
  </article>
</template>


<script setup lang="ts">
defineProps<{
  center: {
    id: number
    name: string
    city?: string
    address?: string
    phone?: string
    email?: string
    description?: string
    created_at?: string
  }
}>()

function formatDate(value?: string) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  })
}
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 18px;
  padding: 16px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  box-shadow: 0 10px 26px rgba(0,0,0,.06);
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
  display: flex;
  flex-direction: column;
  min-height: 220px;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 34px rgba(0,0,0,.10);
  border-color: rgba(26, 92, 255, 0.25);
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
}

.title {
  margin: 0;
  font-size: 18px;
  line-height: 1.25;
  font-weight: 800;
  color: #111827;
}

.pill {
  font-size: 12px;
  font-weight: 800;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(26, 92, 255, 0.12);
  color: #1a5cff;
  border: 1px solid rgba(26, 92, 255, 0.18);
  white-space: nowrap;
}

.body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.line {
  margin: 0;
  display: flex;
  gap: 6px;
  font-size: 13px;
  line-height: 1.45;
}

.label {
  color: #6b7280;
  font-weight: 600;
}

.value {
  color: #111827;
  font-weight: 500;
  word-break: break-word;
}

.desc {
  margin: 10px 0 0;
  font-size: 13px;
  color: #374151;
  line-height: 1.55;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

.foot {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(17, 24, 39, 0.08);
}

.date {
  font-size: 12px;
  color: #6b7280;
}

.open {
  color: #1a5cff;
  font-weight: 900;
  font-size: 13px;
}
</style>
