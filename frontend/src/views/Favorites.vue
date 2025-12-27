<!-- src/views/Favorites.vue -->
<template>
  <section class="page">
    <header class="head">
      <h1 class="title">Избранные программы</h1>
      <button class="btn" @click="reload" :disabled="favorites.loading">
        {{ favorites.loading ? 'Загрузка…' : 'Обновить' }}
      </button>
    </header>

    <div v-if="favorites.error" class="alert error">
      {{ favorites.error }}
    </div>

    <div v-if="favorites.loading" class="state">Загрузка…</div>

    <div v-else-if="favoritePrograms.length === 0" class="empty">
      У вас пока нет избранных программ.
    </div>

    <div v-else class="grid">
      <ProgramCard
        v-for="p in favoritePrograms"
        :key="p.id"
        :program="p"
        :favorites="favorites.ids"
        @toggle-favorite="favorites.toggle"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import ProgramCard from '@/components/ProgramCard.vue'
import { useFavorites } from '@/stores/favorites'

const favorites = useFavorites()

const favoritePrograms = computed(() => favorites.programs)

async function reload() {
  await favorites.load()
}

onMounted(async () => {
  // Грузим избранное с бэка (только текущего пользователя)
  await favorites.load()
})
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.title {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: rgba(255, 255, 255, 0.92);
}

.btn {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.92);
  cursor: pointer;
  font-weight: 800;
  transition: transform 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.18);
  background: rgba(255, 255, 255, 0.12);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.alert {
  padding: 10px 12px;
  border-radius: 14px;
  font-weight: 800;
  margin-bottom: 12px;
}

.alert.error {
  background: rgba(220, 38, 38, 0.12);
  border: 1px solid rgba(220, 38, 38, 0.25);
  color: rgba(255, 255, 255, 0.92);
}

.state {
  text-align: center;
  padding: 26px 10px;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 800;
}

.empty {
  padding: 18px 14px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.88);
  font-weight: 800;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
</style>
