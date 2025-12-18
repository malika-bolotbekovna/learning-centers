<template>
  <aside class="card" style="padding:16px; position:sticky; top:16px;">
    <div style="display:grid; gap:12px;">
      <div>
        <div style="font-weight:600; margin-bottom:6px;">Категория</div>
        <select class="select" v-model="category">
          <option value="">Все</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div>
        <div style="font-weight:600; margin-bottom:6px;">Формат</div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button :class="['btn','ghost']" @click="toggleFormat('online')" :aria-pressed="formats.online">Онлайн</button>
          <button :class="['btn','ghost']" @click="toggleFormat('offline')" :aria-pressed="formats.offline">Оффлайн</button>
        </div>
      </div>
      <div>
        <div style="font-weight:600; margin-bottom:6px;">Цена</div>
        <div style="display:flex; gap:8px;">
          <input class="input" type="number" placeholder="от" v-model.number="minPrice">
          <input class="input" type="number" placeholder="до" v-model.number="maxPrice">
        </div>
      </div>
      <button class="btn" @click="apply">Применить</button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
const props = defineProps<{ categories: {id:number; name:string}[] }>()
const emit = defineEmits<{(e:'filter', payload:any):void}>()
const category = ref<number|''>('')
const formats = reactive({ online:false, offline:false })
const minPrice = ref<number|undefined>()
const maxPrice = ref<number|undefined>()
const toggleFormat = (k:'online'|'offline') => formats[k] = !formats[k]
const apply = () => emit('filter', {
  category: category.value || undefined,
  format: formats.online && formats.offline ? undefined : (formats.online ? 'online' : (formats.offline ? 'offline' : undefined)),
  price_gte: minPrice.value || undefined,
  price_lte: maxPrice.value || undefined,
})
</script>
