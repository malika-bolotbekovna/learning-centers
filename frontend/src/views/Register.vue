<template>
  <section class="container">
    <h1>Регистрация</h1>
    <form @submit.prevent="submit">
      <input v-model="username" placeholder="Логин" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button>Создать</button>
    </form>
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
async function submit(){
  await auth.register(username.value, email.value, password.value)
  router.push('/')
}
</script>
<style scoped>.container{max-width:640px;margin:0 auto;padding:24px}</style>
