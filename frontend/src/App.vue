<template>
  <div class="app-layout">
    <header class="site-header">
      <div class="container header-inner">
        <RouterLink class="brand" to="/">Learning Centers</RouterLink>

        <nav class="nav">
          <RouterLink to="/">Главная</RouterLink>
          <RouterLink to="/centers">Центры</RouterLink>
          <RouterLink to="/favorites">Избранное</RouterLink>
          <RouterLink to="/admin">Админ</RouterLink>

          <!-- НЕ авторизован -->
          <template v-if="!isAuth">
            <RouterLink to="/login">Войти</RouterLink>
            <RouterLink class="btn ghost" to="/register">Регистрация</RouterLink>
          </template>

          <!-- Авторизован -->
          <template v-else>
            <RouterLink class="user-link" to="/profile" title="Открыть профиль">
              <span class="user-name">{{ auth.user?.username }}</span>
              <span class="user-role" v-if="auth.user?.role">({{ auth.user.role }})</span>
            </RouterLink>

            <button class="btn ghost" @click="onLogout">Выйти</button>
          </template>
        </nav>
      </div>
    </header>

    <main class="container page">
      <router-view />
    </main>

    <!-- Footer under all pages -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/stores/auth";
import AppFooter from "@/components/AppFooter.vue";

const router = useRouter();
const auth = useAuth();

const isAuth = computed(() => auth.user !== null);

function onLogout() {
  auth.logout();
  router.push("/login");
}

/* чтобы после перезагрузки страницы пользователь подтягивался */
onMounted(() => {
  if (!auth.user && localStorage.getItem("access")) {
    auth.fetchMe().catch(() => auth.logout());
  }
});
</script>

<style>
html, body, #app {
  height: 100%;
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* важно: main занимает всё свободное место, футер уходит вниз */
.page {
  flex: 1;
}
</style>
