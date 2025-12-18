<template>
  <section class="container">
    <h1>Профиль</h1>
    <pre>{{ user }}</pre>
  </section>
</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuth } from '../stores/auth'
const auth = useAuth()
const { user } = storeToRefs(auth)
</script>
<style scoped>.container{max-width:800px;margin:0 auto;padding:24px}</style>
