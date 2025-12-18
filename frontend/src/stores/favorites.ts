// src/stores/favorites.ts
import { defineStore } from 'pinia'

type FavoritesState = {
  ids: number[]
}

export const useFavorites = defineStore('favorites', {
  state: (): FavoritesState => ({
    ids: [],
  }),

  actions: {
    // переключить избранное для программы
    toggle(id: number) {
      if (this.ids.includes(id)) {
        this.ids = this.ids.filter((x) => x !== id)
      } else {
        this.ids.push(id)
      }
      // опционально — храним в localStorage
      localStorage.setItem('favorites', JSON.stringify(this.ids))
    },

    // опционально — загрузить избранное из localStorage
    loadFromStorage() {
      const raw = localStorage.getItem('favorites')
      if (!raw) return

      try {
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) {
          this.ids = parsed
            .map((x) => Number(x))
            .filter((x) => Number.isInteger(x) && x > 0)
        }
      } catch {
        // если сломанные данные — просто игнорируем
      }
    },
  },
})
