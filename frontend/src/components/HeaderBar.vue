<template>
  <header class="container" style="display:flex; align-items:center; gap:16px;">
    <div style="font-weight:700; font-size:20px;">Learning Centers</div>
    <div style="margin-left:auto; display:flex; gap:10px; width:min(600px, 60%);">
      <input class="input" v-model="q" placeholder="Поиск по курсам, центрам..." @keyup.enter="emitSearch" />
      <select class="select" v-model="sort" @change="emitSearch">
        <option value="-rating">По рейтингу</option>
        <option value="-reviews_count">По отзывам</option>
        <option value="price">Цена ↑</option>
        <option value="-price">Цена ↓</option>
      </select>
      <button class="btn" @click="emitSearch">Найти</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const q = ref('')
const sort = ref('-rating')
const emit = defineEmits<{ (e:'search', payload:{ q:string; ordering:string }):void }>()
const emitSearch = () => emit('search', { q: q.value.trim(), ordering: sort.value })
</script>
