/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  // добавляй свои VITE_* тут
}
interface ImportMeta {
  readonly env: ImportMetaEnv
}
