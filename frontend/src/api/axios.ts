// axios.ts
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// Эндпоинты, куда НЕ нужно добавлять Authorization
const AUTH_WHITELIST = [
  '/auth/token/',          // логин
  '/auth/token/refresh/',  // рефреш
  '/auth/register/',       // регистрация (проверь свой путь на бэке)
  // сюда можешь добавить ещё публичные эндпоинты, если есть
]

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const url = config.url || ''

  const isWhitelisted = AUTH_WHITELIST.some((path) => url.startsWith(path))

  if (!isWhitelisted) {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original: any = error.config

    // если вообще нет исходного конфига — дальше делать нечего
    if (!original) {
      return Promise.reject(error)
    }

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      const refresh = localStorage.getItem('refresh')

      if (refresh) {
        try {
          // используем "сырой" axios, чтобы не попасть в этот же интерсептор
          const { data } = await axios.post(
            `${import.meta.env.VITE_API_URL}/auth/token/refresh/`,
            { refresh }
          )

          // сохранили новый access
          localStorage.setItem('access', data.access)

          // подменили заголовок и повторили оригинальный запрос
          original.headers = original.headers || {}
          original.headers.Authorization = `Bearer ${data.access}`

          return api(original)
        } catch (refreshError) {
          // refresh тоже протух/недействителен — выкидываем токены
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api
