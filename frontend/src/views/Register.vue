<template>
  <section class="container">
    <div class="box">
      <h1 class="title">Регистрация</h1>

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
          <label class="label">Email</label>
          <input
            v-model="email"
            class="input"
            type="email"
            placeholder="Введите email"
            autocomplete="email"
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
            autocomplete="new-password"
            required
          />
        </div>

        <button class="btn">
          Создать
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
const email = ref('')
const password = ref('')

const auth = useAuth()
const router = useRouter()

async function submit() {
  await auth.register(username.value, email.value, password.value)
  router.push('/')
}
</script>

<style scoped>
.container {
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
}

.box {
  width: 100%;
  max-width: 420px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
}

.title {
  color: #000;
}

.form {
  margin-top: 16px;
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
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

  background-color: #ffffff !important;
  color: #111827;

  color-scheme: light; /* ключевая строка */
}

.input::placeholder {
  color: #6b7280;
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
