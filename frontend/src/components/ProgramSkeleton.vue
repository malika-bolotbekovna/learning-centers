<template>
  <div class="card" style="padding:14px; height:160px; position:relative; overflow:hidden;">
    <div class="shimmer" />
  </div>
</template>
<style scoped>
.shimmer {
  position:absolute; inset:0;
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.12) 50%, rgba(255,255,255,0.04) 100%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}
@keyframes shimmer { 0%{background-position: 200% 0;} 100%{background-position: -200% 0;} }
</style>
