<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1 class="title">Профиль</h1>
        <p class="subtitle">Ваши данные аккаунта</p>
      </div>

      <div class="page__actions">
        <button class="btn" @click="loadMe" :disabled="loading">
          {{ loading ? "Обновляю..." : "Обновить" }}
        </button>
      </div>
    </header>

    <div v-if="error" class="alert alert--danger">{{ error }}</div>

    <div v-if="!me && !loading" class="card">
      <div class="muted">Профиль не загружен.</div>
    </div>

    <div v-else class="grid">
      <!-- Summary -->
      <div class="card">
        <h2 class="card__title">Основное</h2>

        <div v-if="loading" class="muted">Загрузка...</div>

        <div v-else class="kv">
          <div class="kv__row">
            <div class="kv__k">ID</div>
            <div class="kv__v">{{ me?.id }}</div>
          </div>
          <div class="kv__row">
            <div class="kv__k">Username</div>
            <div class="kv__v">{{ me?.username }}</div>
          </div>
          <div class="kv__row">
            <div class="kv__k">Email</div>
            <div class="kv__v">{{ me?.email }}</div>
          </div>
          <div class="kv__row">
            <div class="kv__k">Role</div>
            <div class="kv__v">
              <span class="pill">{{ me?.role }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit -->
      <div class="card">
        <h2 class="card__title">Редактирование</h2>

        <form class="form" @submit.prevent="save" v-if="me">
          <div class="form__row">
            <label class="label">Username</label>
            <input v-model.trim="form.username" class="input" autocomplete="username" />
          </div>

          <div class="form__row">
            <label class="label">Email</label>
            <input v-model.trim="form.email" class="input" type="email" autocomplete="email" />
          </div>

          <div class="muted small">
            Роль обычно редактируется только админом, поэтому она здесь только для просмотра.
          </div>

          <div class="form__actions">
            <button class="btn btn--primary" type="submit" :disabled="saving || !isDirty">
              {{ saving ? "Сохраняю..." : "Сохранить" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="reset" :disabled="saving || !me">
              Сбросить
            </button>
          </div>
        </form>

        <div v-else class="muted">Сначала загрузите профиль.</div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import api from "@/api/axios";

type Role = "USER" | "ADMIN";

interface Me {
  id: number;
  username: string;
  email: string;
  role: Role;
}

const ME_ENDPOINT = "/auth/me/"; // если у тебя другое — поменяй (например "/users/me/")

const me = ref<Me | null>(null);
const loading = ref(false);
const saving = ref(false);
const error = ref<string | null>(null);

const form = reactive({
  username: "",
  email: "",
});

const initial = reactive({
  username: "",
  email: "",
});

const isDirty = computed(() => {
  return form.username !== initial.username || form.email !== initial.email;
});

function normalizeApiError(err: any): string {
  const status = err?.response?.status;
  const data = err?.response?.data;

  if (status === 401) return "Не авторизованы (401). Войдите заново.";
  if (status === 403) return "Нет прав (403).";
  if (data?.detail) return String(data.detail);

  if (data && typeof data === "object") {
    const firstKey = Object.keys(data)[0];
    if (firstKey) {
      const v = data[firstKey];
      return `${firstKey}: ${Array.isArray(v) ? v.join(", ") : String(v)}`;
    }
  }
  return "Ошибка запроса.";
}

function syncFormFromMe() {
  if (!me.value) return;
  form.username = me.value.username || "";
  form.email = me.value.email || "";

  initial.username = form.username;
  initial.email = form.email;
}

async function loadMe() {
  loading.value = true;
  error.value = null;

  try {
    const { data } = await api.get<Me>(ME_ENDPOINT);
    me.value = data;
    syncFormFromMe();
  } catch (e: any) {
    error.value = normalizeApiError(e);
  } finally {
    loading.value = false;
  }
}

function reset() {
  form.username = initial.username;
  form.email = initial.email;
}

async function save() {
  if (!me.value) return;

  saving.value = true;
  error.value = null;

  try {
    const payload: Partial<Pick<Me, "username" | "email">> = {
      username: form.username,
      email: form.email,
    };

    const { data } = await api.patch<Me>(ME_ENDPOINT, payload);
    me.value = data;
    syncFormFromMe();
  } catch (e: any) {
    error.value = normalizeApiError(e);
  } finally {
    saving.value = false;
  }
}

onMounted(loadMe);
</script>

<style scoped>
.page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 28px 18px 60px;
  color: #0f172a;
}

.page::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(900px 500px at 20% 10%, rgba(59,130,246,0.18), transparent 60%),
    radial-gradient(900px 500px at 80% 0%, rgba(16,185,129,0.14), transparent 55%),
    linear-gradient(180deg, #0b1020 0%, #070a12 100%);
}

.page__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.title {
  font-size: 30px;
  line-height: 1.15;
  margin: 0;
  letter-spacing: -0.02em;
  color: #eef2ff;
}

.subtitle {
  margin: 10px 0 0;
  color: rgba(226, 232, 240, 0.75);
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.card {
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(255, 255, 255, 0.98);
  border-radius: 16px;
  padding: 16px;
  box-shadow:
    0 18px 60px rgba(0, 0, 0, 0.35),
    0 2px 10px rgba(0, 0, 0, 0.18);
}

.card__title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.kv {
  display: grid;
  gap: 10px;
}

.kv__row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 10px;
  align-items: baseline;
}

.kv__k {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

.kv__v {
  font-size: 14px;
  color: #0f172a;
  overflow-wrap: anywhere;
}

.pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  border: 1px solid rgba(148, 163, 184, 0.45);
  background: #f1f5f9;
}

.form {
  display: grid;
  gap: 12px;
}

.form__row {
  display: grid;
  gap: 6px;
}

.label {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

.input {
  width: 100%;
  border: 1px solid #d7deea;
  border-radius: 12px;
  padding: 10px 12px;
  outline: none;
  background: #ffffff;
  font-size: 14px;
  color: #0f172a;
  transition: box-shadow .15s ease, border-color .15s ease;
}

.input:focus {
  border-color: rgba(37, 99, 235, 0.7);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
}

.form__actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 6px;
}

.btn {
  border: 1px solid rgba(148, 163, 184, 0.5);
  background: #ffffff;
  padding: 10px 14px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn--primary {
  border-color: rgba(37, 99, 235, 0.8);
  background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
  color: #fff;
}

.btn--ghost {
  background: #f1f5f9;
  border-color: rgba(148, 163, 184, 0.35);
  color: #0f172a;
}

.alert {
  border-radius: 14px;
  padding: 12px 12px;
  border: 1px solid;
  font-weight: 700;
  margin-bottom: 14px;
}

.alert--danger {
  background: #fff1f2;
  border-color: #fecdd3;
  color: #7f1d1d;
}

.muted {
  color: #64748b;
  font-size: 13px;
}
.small {
  font-size: 12px;
}

@media (max-width: 980px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
