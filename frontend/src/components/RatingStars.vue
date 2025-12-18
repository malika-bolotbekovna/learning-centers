<template>
  <div style="display:flex; gap:2px;">
    <span v-for="i in 5" :key="i">{{ i <= Math.round(value) ? '★' : '☆' }}</span>
  </div>
</template>
<script setup lang="ts">
defineProps<{ value:number }>()
</script>
