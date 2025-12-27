<template>
  <section class="container">
    <div class="box">
      <h1 class="title">Вход</h1>

      <form class="form" @submit.prevent="submit">
        <div class="field">
          <label class="label">Логин</label>
          <input
            v-model="username"
            class="input"
            placeholder="Введите логин"
            autocomplete="username"
            required
          />
        </div>

        <div class="field">
          <label class="label">Пароль</label>
          <input
            v-model="password"
            class="input"
            type="password"
            placeholder="Введите пароль"
            autocomplete="current-password"
            required
          />
        </div>

        <button class="btn" :disabled="loading">
          {{ loading ? 'Вход…' : 'Войти' }}
        </button>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const loading = ref(false)

const auth = useAuth()
const router = useRouter()

async function submit() {
  try {
    loading.value = true
    await auth.login(username.value, password.value)
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* общий контейнер страницы */
.container {
  min-height: calc(100vh - 64px); /* если есть хедер */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
}

/* сам блок */
.box {
  width: 100%;
  max-width: 420px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
}

/* форма */
.form {
  margin-top: 16px;
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
}

.title {
  color: #000;
}


.label {
  font-size: 14px;
  color: #374151;
}

.input {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
}

.input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.btn {
  margin-top: 8px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 0;
  background: #2563eb;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn:hover {
  background: #1d4ed8;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
