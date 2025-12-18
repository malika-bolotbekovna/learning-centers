import { defineStore } from 'pinia'
import api from '../api/axios'

export const useCatalog = defineStore('catalog', {
  state: () => ({ programs: [] as any[], total: 0, loading:false, q:"", filters: { format:"", category:"", city:"", price_min:"", price_max:"" }, ordering:'-created_at', page:1 }),
  actions: {
    async load() {
      this.loading = true
      const params:any = { search: this.q || undefined, ordering: this.ordering || undefined, page: this.page }
      const f = this.filters
      Object.entries(f).forEach(([k,v]) => { if (v) (params as any)[k] = v })
      const { data } = await api.get('/programs/', { params })
      this.programs = data.results ?? data
      this.total = data.count ?? this.programs.length
      this.loading = false
    }
  }
})
