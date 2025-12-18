<template>
  <section class="container">
    <h1>Избранные программы</h1>

    <div v-if="loading" class="loading">Загрузка…</div>

    <div v-else-if="favoritePrograms.length === 0">
      <p>У вас пока нет избранных программ.</p>
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
import { computed, onMounted, ref } from 'vue'
import { useCatalog } from '@/stores/catalog'
import { useFavorites } from '@/stores/favorites'
import ProgramCard from '@/components/ProgramCard.vue'

const catalog = useCatalog()
const favorites = useFavorites()

const loading = ref(false)

onMounted(async () => {
  loading.value = true

  // подтягиваем избранное из localStorage (safe)
  favorites.loadFromStorage?.()

  // если программы ещё не загружены — грузим
  if (!catalog.programs.length) {
    await catalog.load()
  }

  loading.value = false
})

const favoritePrograms = computed(() =>
  catalog.programs.filter((p) => favorites.ids.includes(p.id))
)
</script>

<style scoped>
.container { max-width: 1100px; margin: 0 auto; padding: 24px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 16px; }
.loading { margin-top: 12px; }
</style>
