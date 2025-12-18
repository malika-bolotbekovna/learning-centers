<template>
  <header class="site-header">
    <div class="container header-inner">
      <RouterLink class="brand" to="/">Learning Centers</RouterLink>
      <nav class="nav">
        <RouterLink to="/">Главная</RouterLink>
        <RouterLink to="/programs">Программы</RouterLink>
        <RouterLink to="/centers">Центры</RouterLink>
        <RouterLink to="/favorites">Избранное</RouterLink>
        <RouterLink to="/reviews">Отзывы</RouterLink>
        <RouterLink to="/admin">Админ</RouterLink>
        <RouterLink to="/login">Войти</RouterLink>
        <RouterLink class="btn ghost" to="/register">Регистрация</RouterLink>
      </nav>
    </div>
  </header>
  <main class="container page">
    <router-view />
  </main>
</template>

<script setup lang="ts">
</script>
