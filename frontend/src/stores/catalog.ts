import { defineStore } from 'pinia'
import api from '../api/axios'

export const useCatalog = defineStore('catalog', {
  state: () => ({ programs: [] as any[], total: 0, loading:false, q:"", filters: { program_format:"", category:"", city:"", price:"" }, ordering:'-created_at', page:1 }),
  actions: {
    async load() {
      this.loading = true
      try {
        const params:any = { search: this.q || undefined, ordering: this.ordering || undefined, page: this.page }
        const f = this.filters
        Object.entries(f).forEach(([k,v]) => { if (v) (params as any)[k] = v })

        const { data } = await api.get('/programs/', { params })
        this.programs = data.results ?? data
        this.total = data.count ?? this.programs.length
      } catch (e: any) {
        if (e?.response?.status === 404) {
          this.programs = []
          this.total = 0
        } else {
          throw e
        }
      } finally {
        this.loading = false
      }
    }
  }
})
