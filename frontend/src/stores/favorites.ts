// src/stores/favorites.ts
import { defineStore } from 'pinia'
import api from '@/api/axios'
import type { Program } from '@//types/program'

type FavoriteItem = {
  id: number
  created_at: string
  program: Program
}

type FavoritesState = {
  items: FavoriteItem[]
  loading: boolean
  error: string | null
}

export const useFavorites = defineStore('favorites', {
  state: (): FavoritesState => ({
    items: [],
    loading: false,
    error: null,
  }),

  getters: {
    ids: (state) => state.items.map((f) => f.program.id),
    programs: (state) => state.items.map((f) => f.program),
    byProgramId: (state) => {
      const m = new Map<number, FavoriteItem>()
      for (const it of state.items) m.set(it.program.id, it)
      return m
    },
  },

  actions: {
    async load() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/favorites/')
        this.items = Array.isArray(data) ? data : (data?.results ?? [])
      } catch (e: any) {
        this.error = e?.response?.data?.detail || 'Не удалось загрузить избранное'
        this.items = []
      } finally {
        this.loading = false
      }
    },

    async add(programId: number) {
      this.error = null
      try {
        const { data } = await api.post('/favorites/', { program_id: programId })
        // data = созданный Favorite (по твоему serializer)
        this.items.unshift(data)
      } catch (e: any) {
        // если есть unique_together(user, program) — будет 400
        this.error = e?.response?.data?.detail || 'Не удалось добавить в избранное'
        // на всякий случай обновим список
        await this.load()
      }
    },

    async remove(programId: number) {
      this.error = null
      const fav = this.byProgramId.get(programId)
      if (!fav) return

      try {
        await api.delete(`/favorites/${fav.id}/`)
        this.items = this.items.filter((x) => x.id !== fav.id)
      } catch (e: any) {
        this.error = e?.response?.data?.detail || 'Не удалось убрать из избранного'
        await this.load()
      }
    },

    async toggle(programId: number) {
      if (this.byProgramId.get(programId)) {
        await this.remove(programId)
      } else {
        await this.add(programId)
      }
    },

    // при выходе чистим, чтобы следующий пользователь не видел чужое в UI
    reset() {
      this.items = []
      this.loading = false
      this.error = null
    },
  },
})
