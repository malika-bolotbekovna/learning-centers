<template>
  <section class="container">
    <h1>Каталог программ</h1>

    <!-- Фильтры -->
    <div class="controls">
      <input
        v-model="catalog.q"
        placeholder="Поиск по названию, теме, городу"
        @input="catalog.load"
      />

      <select v-model="catalog.filters.format" @change="catalog.load">
        <option value="">Формат: любой</option>
        <option value="ONLINE">Онлайн</option>
        <option value="OFFLINE">Оффлайн</option>
        <option value="MIXED">Смешанный</option>
      </select>

      <select v-model="catalog.ordering" @change="catalog.load">
        <option value="-created_at">Сначала новые</option>
        <option value="-rating_avg">Рейтинг ↓</option>
      </select>
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
        @toggle-favorite="favorites.toggle"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useCatalog } from '@/stores/catalog'
import { useFavorites } from '@/stores/favorites'
import ProgramCard from '@/components/ProgramCard.vue'

const catalog = useCatalog()
const favorites = useFavorites()

onMounted(() => {
  // первая загрузка
  if (!catalog.programs.length) {
    catalog.load()
  }
  favorites.loadFromStorage?.()
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
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.loading {
  margin-top: 30px;
  text-align: center;
  font-size: 16px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
