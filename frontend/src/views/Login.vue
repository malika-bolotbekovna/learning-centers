<template>
  <section class="container">
    <h1>Вход</h1>
    <form @submit.prevent="submit">
      <input v-model="username" placeholder="Логин" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button>Войти</button>
    </form>
  </section>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../stores/auth'
import { useRouter } from 'vue-router'
const username = ref('')
const password = ref('')
const auth = useAuth()
const router = useRouter()
async function submit(){
  await auth.login(username.value, password.value)
  router.push('/')
}
</script>
<style scoped>.container{max-width:640px;margin:0 auto;padding:24px}</style>
