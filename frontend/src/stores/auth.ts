import { defineStore } from 'pinia'
import api from '../api/axios'

export const useAuth = defineStore('auth', {
  state: () => ({ user: null as null | { id:number; username:string; email:string; role:string }, loading:false, error:null as string|null }),
  actions: {
    async register(username:string, email:string, password:string) {
      await api.post('/auth/register/', { username, email, password })
      return this.login(username, password)
    },
    async login(username:string, password:string) {
      const { data } = await api.post('/auth/token/', { username, password })
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      await this.fetchMe()
    },
    async fetchMe() {
      const { data } = await api.get('/auth/me/')
      this.user = data
    },
    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.user = null
    }
  }
})
