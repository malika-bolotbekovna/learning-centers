<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1 class="title">Админ-панель</h1>
        <p class="subtitle">Управление центрами, категориями и программами</p>
      </div>

      <div class="page__meta" v-if="authUser">
        <div class="chip">Пользователь: <b>{{ authUser.username }}</b></div>
        <div class="chip">Роль: <b>{{ authUser.role }}</b></div>
      </div>
    </header>

    <div v-if="!authUser" class="alert alert--warning">
      Вы не авторизованы. Войдите в систему.
    </div>

    <div v-else-if="!isAdmin" class="alert alert--danger">
      Доступ запрещён. Эта страница доступна только для роли <b>ADMIN</b>.
    </div>

    <div v-else class="grid">
      <!-- Centers -->
      <div class="card">
        <div class="card__head">
          <h2 class="card__title">Центры</h2>
          <button class="btn" @click="reloadAll" :disabled="loadingAny">
            Обновить
          </button>
        </div>

        <form class="form" @submit.prevent="createCenter" aria-label="Создать центр">
          <div class="form__row">
            <label class="label">Name</label>
            <input v-model="centerForm.name" class="input" required />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Description</label>
            <textarea v-model="centerForm.description" class="textarea" rows="6"></textarea>
          </div>

          <div class="form__row">
            <label class="label">Rating avg</label>
            <input v-model.number="centerForm.rating_avg" class="input" type="number" min="0" step="0.1" />
          </div>

          <div class="form__row">
            <label class="label">City</label>
            <input v-model="centerForm.city" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Address</label>
            <input v-model="centerForm.address" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Phone</label>
            <input v-model="centerForm.phone" class="input" placeholder="+996..." />
          </div>

          <div class="form__row">
            <label class="label">Email</label>
            <input v-model="centerForm.email" class="input" type="email" placeholder="info@..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Website</label>
            <input v-model="centerForm.website" class="input" placeholder="https://..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social vk</label>
            <input v-model="centerForm.social_vk" class="input" placeholder="https://vk.com/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social instagram</label>
            <input v-model="centerForm.social_instagram" class="input" placeholder="https://instagram.com/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social telegram</label>
            <input v-model="centerForm.social_telegram" class="input" placeholder="https://t.me/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="checkbox">
              <input type="checkbox" v-model="centerForm.is_active" />
              <span>Is active</span>
            </label>
          </div>

          <div class="form__actions">
            <button class="btn btn--primary" type="submit" :disabled="creating.center">
              {{ creating.center ? "Создаю..." : "Создать центр" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="resetCenterForm" :disabled="creating.center">
              Очистить
            </button>
          </div>
        </form>

        <div class="divider"></div>

        <div class="list">
          <div class="list__head">
            <div class="muted">Всего: {{ centers.length }}</div>
            <div v-if="loading.centers" class="muted">Загрузка...</div>
          </div>

          <div v-if="centersError" class="alert alert--danger">{{ centersError }}</div>

          <div v-for="c in centers" :key="c.id" class="item">
            <div class="item__main">
              <div class="item__title">{{ c.name }}</div>
              <div class="item__meta">
                <span v-if="c.city">{{ c.city }}</span>
                <span v-if="c.address">• {{ c.address }}</span>
              </div>
            </div>

            <div class="item__actions actions-col">
              <button class="btn btn--ghost" @click="openEditCenter(c)">
                Редактировать
              </button>
              <button class="btn btn--danger" @click="deleteCenter(c.id)" :disabled="deletingIds.centers.has(c.id)">
                {{ deletingIds.centers.has(c.id) ? "Удаляю..." : "Удалить" }}
              </button>
            </div>
          </div>

          <div v-if="!loading.centers && centers.length === 0" class="muted">
            Центров пока нет.
          </div>
        </div>
      </div>

      <!-- Categories -->
      <div class="card">
        <div class="card__head">
          <h2 class="card__title">Категории</h2>
        </div>

        <form class="form" @submit.prevent="createCategory" aria-label="Создать категорию">
          <div class="form__row">
            <label class="label">Название</label>
            <input v-model="categoryForm.name" class="input" placeholder="Например: Программирование" required />
          </div>
          <div class="form__row">
            <label class="label">Slug</label>
            <input v-model="categoryForm.slug" class="input" placeholder="programming" required />
          </div>

          <div class="form__actions">
            <button class="btn btn--primary" type="submit" :disabled="creating.category">
              {{ creating.category ? "Создаю..." : "Создать категорию" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="resetCategoryForm" :disabled="creating.category">
              Очистить
            </button>
          </div>
        </form>

        <div class="divider"></div>

        <div class="list">
          <div class="list__head">
            <div class="muted">Всего: {{ categories.length }}</div>
            <div v-if="loading.categories" class="muted">Загрузка...</div>
          </div>

          <div v-if="categoriesError" class="alert alert--danger">{{ categoriesError }}</div>

          <div v-for="cat in categories" :key="cat.id" class="item">
            <div class="item__main">
              <div class="item__title">{{ cat.name }}</div>
              <div class="item__meta">{{ cat.slug }}</div>
            </div>

            <div class="item__actions">
              <button class="btn btn--danger" @click="deleteCategory(cat.id)" :disabled="deletingIds.categories.has(cat.id)">
                {{ deletingIds.categories.has(cat.id) ? "Удаляю..." : "Удалить" }}
              </button>
            </div>
          </div>

          <div v-if="!loading.categories && categories.length === 0" class="muted">
            Категорий пока нет.
          </div>
        </div>
      </div>

      <!-- Programs -->
      <div class="card grid__span2">
        <div class="card__head">
          <h2 class="card__title">Программы</h2>

          <div style="display:flex; gap:10px; align-items:center;">
            <select
              class="select"
              v-model.number="programCenterFilter"
              @change="loadPrograms"
            >
              <option :value="null">Все центры</option>
              <option v-for="c in centers" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
            </select>

            <button class="btn" @click="loadPrograms" :disabled="loading.programs">
              Обновить
            </button>
          </div>
        </div>

        <!-- Create program -->
        <form class="form form--grid" @submit.prevent="createProgram" aria-label="Создать программу">
          <div class="form__row">
            <label class="label">Center</label>
            <select v-model.number="programForm.center_id" class="select" required>
              <option :value="null" disabled>---------</option>
              <option v-for="c in centers" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Title</label>
            <input v-model.trim="programForm.title" class="input" required />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Description</label>
            <textarea v-model.trim="programForm.description" class="textarea" required></textarea>
          </div>

          <div class="form__row">
            <label class="label">Category</label>
            <select v-model.number="programForm.category_id" class="select" required>
              <option :value="null" disabled>---------</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Topic</label>
            <input v-model.trim="programForm.topic" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Format</label>
            <select v-model="programForm.format" class="select">
              <option v-for="o in programFormatOptions" :key="o.value" :value="o.value">
                {{ o.label }}
              </option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Price</label>
            <input v-model.number="programForm.price" class="input" type="number" min="0" step="0.01" />
          </div>

          <div class="form__row">
            <label class="label">Currency</label>
            <input v-model.trim="programForm.currency" class="input" placeholder="KGS" />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Schedule</label>
            <input v-model.trim="programForm.schedule" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Age min</label>
            <input v-model.number="programForm.age_min" class="input" type="number" min="0" />
          </div>

          <div class="form__row">
            <label class="label">Age max</label>
            <input v-model.number="programForm.age_max" class="input" type="number" min="0" />
          </div>

          <div class="form__row form__row--full checkbox-row">
            <input id="is_active" v-model="programForm.is_active" type="checkbox" />
            <label for="is_active" class="label" style="margin:0;">Is active</label>
          </div>

          <div class="form__actions form__actions--full">
            <button class="btn btn--primary" type="submit" :disabled="creating.program">
              {{ creating.program ? "Создаю..." : "Создать программу" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="resetProgramForm" :disabled="creating.program">
              Очистить
            </button>
          </div>
        </form>

        <div class="divider"></div>

        <div class="list">
          <div class="list__head">
            <div class="muted">Всего: {{ programs.length }}</div>
            <div v-if="loading.programs" class="muted">Загрузка...</div>
          </div>

          <div v-if="programsError" class="alert alert--danger">{{ programsError }}</div>

          <div class="programs-grid">
            <div v-for="p in programs" :key="p.id" class="item program-item">
              <div class="item__main">
                <div class="item__title">{{ p.title }}</div>

                <div class="item__meta program-meta">
                  <div class="meta-row">
                    <span class="meta-label">Центр:</span>
                    <span class="meta-value">
                      {{ p.center?.name || `Center #${p.center?.id ?? "—"}` }}
                      <span class="meta-muted" v-if="p.center">
                        ({{ p.center.city || "—" }}, {{ p.center.address || "—" }})
                      </span>
                    </span>
                  </div>

                  <div class="meta-row">
                    <span class="meta-label">Категория:</span>
                    <span class="meta-value">
                      {{ p.category?.name || `Category #${p.category?.id ?? "—"}` }}
                    </span>
                  </div>

                  <div class="meta-row" v-if="p.topic">
                    <span class="meta-label">Топик:</span>
                    <span class="meta-value">{{ p.topic }}</span>
                  </div>

                  <div class="meta-row">
                    <span class="meta-label">Формат:</span>
                    <span class="meta-value">{{ formatLabel(p.format) }}</span>
                  </div>

                  <div class="meta-row">
                    <span class="meta-label">Цена:</span>
                    <span class="meta-price">
                      {{ formatPrice(p.price) }} {{ p.currency || "KGS" }}
                    </span>
                  </div>

                  <div class="meta-row" v-if="p.schedule">
                    <span class="meta-label">График:</span>
                    <span class="meta-value">{{ p.schedule }}</span>
                  </div>

                  <div class="meta-row" v-if="p.age_min != null || p.age_max != null">
                    <span class="meta-label">Возраст:</span>
                    <span class="meta-value">
                      <span v-if="p.age_min != null">от {{ p.age_min }}</span>
                      <span v-if="p.age_min != null && p.age_max != null"> </span>
                      <span v-if="p.age_max != null"> до {{ p.age_max }}</span>
                    </span>
                  </div>

                  <div class="meta-row">
                    <span class="meta-label">Активна:</span>
                    <span class="meta-value">{{ p.is_active ? "Да" : "Нет" }}</span>
                  </div>
                </div>
              </div>

              <div class="item__actions actions-col">
                <button class="btn btn--ghost" @click="openEditProgram(p)">
                  Редактировать
                </button>

                <button
                  class="btn btn--danger"
                  @click="deleteProgram(p.id)"
                  :disabled="deletingIds.programs.has(p.id)"
                >
                  {{ deletingIds.programs.has(p.id) ? "Удаляю..." : "Удалить" }}
                </button>
              </div>
            </div>
          </div>

          <div v-if="!loading.programs && programs.length === 0" class="muted">
            Программ пока нет.
          </div>
        </div>
      </div>

      <!-- Global errors -->
      <div v-if="globalError" class="alert alert--danger grid__span2">
        {{ globalError }}
      </div>
    </div>

    <!-- Edit Center Modal -->
    <div v-if="editCenter.open" class="modal" @mousedown.self="closeEditCenter">
      <div class="modal__card" role="dialog" aria-modal="true">
        <div class="modal__head">
          <h3 class="modal__title">Редактировать центр</h3>
          <button class="btn btn--ghost" @click="closeEditCenter">Закрыть</button>
        </div>

        <form class="form" @submit.prevent="saveEditCenter">
          <div class="form__row">
            <label class="label">Название</label>
            <input v-model.trim="editCenter.form.name" class="input" required />
          </div>
          <div class="form__row">
            <label class="label">Город</label>
            <input v-model.trim="editCenter.form.city" class="input" />
          </div>
          <div class="form__row">
            <label class="label">Адрес</label>
            <input v-model.trim="editCenter.form.address" class="input" />
          </div>
          <div class="form__row">
            <label class="label">Описание</label>
            <textarea v-model.trim="editCenter.form.description" class="textarea"></textarea>
          </div>

          <div class="form__actions">
            <button class="btn btn--primary" type="submit" :disabled="editCenter.saving">
              {{ editCenter.saving ? "Сохраняю..." : "Сохранить" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="closeEditCenter" :disabled="editCenter.saving">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Program Modal -->
    <div v-if="editProgram.open" class="modal" @mousedown.self="closeEditProgram">
      <div class="modal__card" role="dialog" aria-modal="true">
        <div class="modal__head">
          <h3 class="modal__title">Редактировать программу</h3>
          <button class="btn btn--ghost" @click="closeEditProgram">Закрыть</button>
        </div>

        <form class="form form--grid" @submit.prevent="saveEditProgram">
          <div class="form__row">
            <label class="label">Center</label>
            <select v-model.number="editProgram.form.center_id" class="select" required>
              <option :value="null" disabled>---------</option>
              <option v-for="c in centers" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Title</label>
            <input v-model.trim="editProgram.form.title" class="input" required />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Description</label>
            <textarea v-model.trim="editProgram.form.description" class="textarea" required></textarea>
          </div>

          <div class="form__row">
            <label class="label">Category</label>
            <select v-model.number="editProgram.form.category_id" class="select" required>
              <option :value="null" disabled>---------</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Topic</label>
            <input v-model.trim="editProgram.form.topic" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Format</label>
            <select v-model="editProgram.form.format" class="select">
              <option v-for="o in programFormatOptions" :key="o.value" :value="o.value">
                {{ o.label }}
              </option>
            </select>
          </div>

          <div class="form__row">
            <label class="label">Price</label>
            <input v-model.number="editProgram.form.price" class="input" type="number" min="0" step="0.01" />
          </div>

          <div class="form__row">
            <label class="label">Currency</label>
            <input v-model.trim="editProgram.form.currency" class="input" placeholder="KGS" />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Schedule</label>
            <input v-model.trim="editProgram.form.schedule" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Age min</label>
            <input v-model.number="editProgram.form.age_min" class="input" type="number" min="0" />
          </div>

          <div class="form__row">
            <label class="label">Age max</label>
            <input v-model.number="editProgram.form.age_max" class="input" type="number" min="0" />
          </div>

          <div class="form__row form__row--full checkbox-row">
            <input id="edit_is_active" v-model="editProgram.form.is_active" type="checkbox" />
            <label for="edit_is_active" class="label" style="margin:0;">Is active</label>
          </div>

          <div class="form__actions form__actions--full">
            <button class="btn btn--primary" type="submit" :disabled="editProgram.saving">
              {{ editProgram.saving ? "Сохраняю..." : "Сохранить" }}
            </button>
            <button class="btn btn--ghost" type="button" @click="closeEditProgram" :disabled="editProgram.saving">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Edit Center Modal -->
    <div v-if="editCenterOpen" class="modalOverlay" @click.self="closeEditCenter">
      <div class="modal modal--wide">
        <h3 class="modalTitle">Редактировать центр</h3>

        <div class="form form--grid">
          <div class="form__row">
            <label class="label">Name</label>
            <input v-model="centerEditForm.name" class="input" required />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Description</label>
            <textarea v-model="centerEditForm.description" class="textarea" rows="6"></textarea>
          </div>

          <div class="form__row">
            <label class="label">Rating avg</label>
            <input v-model.number="centerEditForm.rating_avg" class="input" type="number" min="0" step="0.1" />
          </div>

          <div class="form__row">
            <label class="label">City</label>
            <input v-model="centerEditForm.city" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Address</label>
            <input v-model="centerEditForm.address" class="input" />
          </div>

          <div class="form__row">
            <label class="label">Phone</label>
            <input v-model="centerEditForm.phone" class="input" placeholder="+996..." />
          </div>

          <div class="form__row">
            <label class="label">Email</label>
            <input v-model="centerEditForm.email" class="input" type="email" placeholder="info@..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Website</label>
            <input v-model="centerEditForm.website" class="input" placeholder="https://..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social vk</label>
            <input v-model="centerEditForm.social_vk" class="input" placeholder="https://vk.com/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social instagram</label>
            <input v-model="centerEditForm.social_instagram" class="input" placeholder="https://instagram.com/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="label">Social telegram</label>
            <input v-model="centerEditForm.social_telegram" class="input" placeholder="https://t.me/..." />
          </div>

          <div class="form__row form__row--full">
            <label class="checkbox">
              <input type="checkbox" v-model="centerEditForm.is_active" />
              <span>Is active</span>
            </label>
          </div>
        </div>

        <div v-if="centerEditError" class="alert alert--danger" style="margin-top:12px;">
          {{ centerEditError }}
        </div>

        <div class="modalActions">
          <button class="btn" @click="closeEditCenter" :disabled="savingCenter">Закрыть</button>
          <button class="btn btn--primary" @click="saveCenterEdit" :disabled="savingCenter">
            {{ savingCenter ? "Сохраняю..." : "Сохранить" }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import api from "@/api/axios";
import { useAuth } from "@/stores/auth";

type Role = "USER" | "ADMIN";
interface AuthUser { id: number; username: string; email: string; role: Role; }

interface Center {
  id: number
  name: string
  description?: string | null
  rating_avg?: number | null
  city?: string | null
  address?: string | null
  phone?: string | null
  email?: string | null
  website?: string | null
  social_vk?: string | null
  social_instagram?: string | null
  social_telegram?: string | null
  is_active?: boolean
  created_at?: string
}


interface Category { id: number; name: string; slug: string; }

type ProgramFormat = "ONLINE" | "OFFLINE" | "MIXED";

interface Program {
  id: number;
  title: string;
  description?: string | null;
  topic?: string | null;
  format: ProgramFormat;
  price?: number | null;
  currency: string;
  schedule?: string | null;
  age_min?: number | null;
  age_max?: number | null;
  is_active: boolean;
  center: Center;
  category: Category | null;
}

const programFormatOptions: Array<{ value: ProgramFormat; label: string }> = [
  { value: "ONLINE", label: "Онлайн" },
  { value: "OFFLINE", label: "Оффлайн" },
  { value: "MIXED", label: "Смешанный" },
];

function formatLabel(v: ProgramFormat) {
  if (v === "ONLINE") return "Онлайн";
  if (v === "MIXED") return "Смешанный";
  return "Оффлайн";
}

const auth = useAuth();
const authUser = computed<AuthUser | null>(() => (auth as any).user ?? null);
const isAdmin = computed(() => authUser.value?.role === "ADMIN");

const loading = reactive({ centers: false, categories: false, programs: false });
const creating = reactive({ center: false, category: false, program: false });

const deletingIds = reactive({
  centers: new Set<number>(),
  categories: new Set<number>(),
  programs: new Set<number>(),
});

const globalError = ref<string | null>(null);
const centersError = ref<string | null>(null);
const categoriesError = ref<string | null>(null);
const programsError = ref<string | null>(null);
const programCenterFilter = ref<number | null>(null)
const editCenterOpen = ref(false)
const editingCenterId = ref<number | null>(null)
const centers = ref<Center[]>([]);
const categories = ref<Category[]>([]);
const programs = ref<Program[]>([]);

const centerForm = reactive({
  name: '',
  description: '',
  rating_avg: 0 as number | null,
  city: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  social_vk: '',
  social_instagram: '',
  social_telegram: '',
  is_active: true,
})


const centerEditForm = reactive({
  name: '',
  description: '',
  rating_avg: 0 as number | null,
  city: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  social_vk: '',
  social_instagram: '',
  social_telegram: '',
  is_active: true,
})

const savingCenter = ref(false)
const centerEditError = ref<string | null>(null)

const categoryForm = reactive({ name: "", slug: "" });

const programForm = reactive<{
  center_id: number | null;
  title: string;
  description: string;
  category_id: number | null;
  topic: string;
  format: ProgramFormat;
  price: number | null;
  currency: string;
  schedule: string;
  age_min: number | null;
  age_max: number | null;
  is_active: boolean;
}>({
  center_id: null,
  title: "",
  description: "",
  category_id: null,
  topic: "",
  format: "OFFLINE",
  price: null,
  currency: "KGS",
  schedule: "",
  age_min: null,
  age_max: null,
  is_active: true,
});

const ENDPOINTS = { centers: "/centers/", categories: "/categories/", programs: "/programs/" };
const loadingAny = computed(() => loading.centers || loading.categories || loading.programs);

function normalizeApiError(err: any): string {
  const status = err?.response?.status;
  const data = err?.response?.data;

  if (status === 401) return "Не авторизованы (401). Войдите заново.";
  if (status === 403) return "Нет прав (403). Требуется роль ADMIN.";
  if (data?.detail) return String(data.detail);
  if (typeof data === "string") return data;
  if (data && typeof data === "object") {
    const firstKey = Object.keys(data)[0];
    if (firstKey) {
      const v = data[firstKey];
      return `${firstKey}: ${Array.isArray(v) ? v.join(", ") : String(v)}`;
    }
  }
  return "Ошибка запроса.";
}

function formatPrice(value: number | null | undefined) {
  return new Intl.NumberFormat("ru-RU").format(value ?? 0);
}

async function loadCenters() {
  loading.centers = true; centersError.value = null;
  try {
    const { data } = await api.get(ENDPOINTS.centers);
    centers.value = Array.isArray(data) ? data : (data?.results ?? []);
  } catch (e: any) {
    centersError.value = normalizeApiError(e);
  } finally { loading.centers = false; }
}

async function loadCategories() {
  loading.categories = true; categoriesError.value = null;
  try {
    const { data } = await api.get(ENDPOINTS.categories);
    categories.value = Array.isArray(data) ? data : (data?.results ?? []);
  } catch (e: any) {
    categoriesError.value = normalizeApiError(e);
  } finally { loading.categories = false; }
}

async function loadPrograms() {
  loading.programs = true
  programsError.value = null

  try {
    const params: any = { page_size: 50 }

    if (programCenterFilter.value) {
      params.center = programCenterFilter.value
      // если у тебя на бэке center_id → замени на center_id
      // params.center_id = programCenterFilter.value
    }

    const { data } = await api.get(ENDPOINTS.programs, { params })
    programs.value = Array.isArray(data) ? data : (data?.results ?? [])
  } catch (e: any) {
    programsError.value = normalizeApiError(e)
  } finally {
    loading.programs = false
  }
}


async function reloadAll() {
  globalError.value = null;
  await Promise.all([loadCenters(), loadCategories(), loadPrograms()]);
}

function resetCenterForm() {
  centerForm.name = ''
  centerForm.description = ''
  centerForm.rating_avg = 0
  centerForm.city = ''
  centerForm.address = ''
  centerForm.phone = ''
  centerForm.email = ''
  centerForm.website = ''
  centerForm.social_vk = ''
  centerForm.social_instagram = ''
  centerForm.social_telegram = ''
  centerForm.is_active = true
}
function openEditCenter(c: Center) {
  centerEditError.value = null
  editCenterOpen.value = true
  editingCenterId.value = c.id

  centerEditForm.name = c.name || ''
  centerEditForm.description = (c.description ?? '') as any
  centerEditForm.rating_avg = (c.rating_avg ?? 0) as any
  centerEditForm.city = (c.city ?? '') as any
  centerEditForm.address = (c.address ?? '') as any
  centerEditForm.phone = (c.phone ?? '') as any
  centerEditForm.email = (c.email ?? '') as any
  centerEditForm.website = (c.website ?? '') as any
  centerEditForm.social_vk = (c.social_vk ?? '') as any
  centerEditForm.social_instagram = (c.social_instagram ?? '') as any
  centerEditForm.social_telegram = (c.social_telegram ?? '') as any
  centerEditForm.is_active = c.is_active ?? true
}

function closeEditCenter() {
  editCenterOpen.value = false
  editingCenterId.value = null
  centerEditError.value = null
}

async function saveCenterEdit() {
  if (!editingCenterId.value) return
  savingCenter.value = true
  centerEditError.value = null

  try {
    const payload = {
      name: centerEditForm.name,
      description: centerEditForm.description || null,
      rating_avg: centerEditForm.rating_avg ?? 0,
      city: centerEditForm.city || null,
      address: centerEditForm.address || null,
      phone: centerEditForm.phone || null,
      email: centerEditForm.email || null,
      website: centerEditForm.website || null,
      social_vk: centerEditForm.social_vk || null,
      social_instagram: centerEditForm.social_instagram || null,
      social_telegram: centerEditForm.social_telegram || null,
      is_active: !!centerEditForm.is_active,
    }

    const { data } = await api.patch(`${ENDPOINTS.centers}${editingCenterId.value}/`, payload)

    // обновляем в списке
    const idx = centers.value.findIndex(x => x.id === editingCenterId.value)
    if (idx !== -1) centers.value[idx] = data

    closeEditCenter()
  } catch (e: any) {
    centerEditError.value = normalizeApiError(e)
  } finally {
    savingCenter.value = false
  }
}

function resetCategoryForm() { categoryForm.name = ""; categoryForm.slug = ""; }
function resetProgramForm() {
  programForm.center_id = null;
  programForm.title = "";
  programForm.description = "";
  programForm.category_id = null;
  programForm.topic = "";
  programForm.format = "OFFLINE";
  programForm.price = null;
  programForm.currency = "KGS";
  programForm.schedule = "";
  programForm.age_min = null;
  programForm.age_max = null;
  programForm.is_active = true;
}

async function createCenter() {
  globalError.value = null
  creating.center = true
  try {
    const payload = {
      name: centerForm.name,
      description: centerForm.description || null,
      rating_avg: centerForm.rating_avg ?? 0,
      city: centerForm.city || null,
      address: centerForm.address || null,
      phone: centerForm.phone || null,
      email: centerForm.email || null,
      website: centerForm.website || null,
      social_vk: centerForm.social_vk || null,
      social_instagram: centerForm.social_instagram || null,
      social_telegram: centerForm.social_telegram || null,
      is_active: !!centerForm.is_active,
    }

    const { data } = await api.post(ENDPOINTS.centers, payload)
    centers.value.unshift(data)
    resetCenterForm()
  } catch (e: any) {
    globalError.value = normalizeApiError(e)
  } finally {
    creating.center = false
  }
}


async function createCategory() {
  globalError.value = null; creating.category = true;
  try {
    const payload = { name: categoryForm.name, slug: categoryForm.slug };
    const { data } = await api.post(ENDPOINTS.categories, payload);
    categories.value.unshift(data);
    resetCategoryForm();
  } catch (e: any) {
    globalError.value = normalizeApiError(e);
  } finally { creating.category = false; }
}

async function createProgram() {
  globalError.value = null; creating.program = true;
  try {
    if (!programForm.center_id) throw new Error("Выберите центр.");
    if (!programForm.category_id) throw new Error("Выберите категорию.");

    const payload = {
      title: programForm.title,
      description: programForm.description,
      topic: programForm.topic ?? "",
      format: programForm.format,
      price: programForm.price,
      currency: programForm.currency || "KGS",
      schedule: programForm.schedule ?? "",
      age_min: programForm.age_min,
      age_max: programForm.age_max,
      is_active: programForm.is_active,
      center_id: programForm.center_id,
      category_id: programForm.category_id,
    };

    const { data } = await api.post(ENDPOINTS.programs, payload);
    programs.value.unshift(data);
    resetProgramForm();
  } catch (e: any) {
    globalError.value = e?.message && !e?.response ? String(e.message) : normalizeApiError(e);
  } finally { creating.program = false; }
}

async function deleteCenter(id: number) {
  if (!confirm("Удалить центр?")) return;
  globalError.value = null; deletingIds.centers.add(id);
  try {
    await api.delete(`${ENDPOINTS.centers}${id}/`);
    centers.value = centers.value.filter((x) => x.id !== id);
  } catch (e: any) {
    globalError.value = normalizeApiError(e);
  } finally { deletingIds.centers.delete(id); }
}

async function deleteCategory(id: number) {
  if (!confirm("Удалить категорию?")) return;
  globalError.value = null; deletingIds.categories.add(id);
  try {
    await api.delete(`${ENDPOINTS.categories}${id}/`);
    categories.value = categories.value.filter((x) => x.id !== id);
  } catch (e: any) {
    globalError.value = normalizeApiError(e);
  } finally { deletingIds.categories.delete(id); }
}

async function deleteProgram(id: number) {
  if (!confirm("Удалить программу?")) return;
  globalError.value = null; deletingIds.programs.add(id);
  try {
    await api.delete(`${ENDPOINTS.programs}${id}/`);
    programs.value = programs.value.filter((x) => x.id !== id);
  } catch (e: any) {
    globalError.value = normalizeApiError(e);
  } finally { deletingIds.programs.delete(id); }
}

/* ------------------------- EDIT CENTER ------------------------- */
const editCenter = reactive<{
  open: boolean;
  id: number | null;
  saving: boolean;
  form: { name: string; city: string; address: string; description: string };
}>({
  open: false,
  id: null,
  saving: false,
  form: { name: "", city: "", address: "", description: "" },
});


async function saveEditCenter() {
  if (!editCenter.id) return;
  editCenter.saving = true;
  globalError.value = null;
  try {
    const payload = {
      name: editCenter.form.name,
      city: editCenter.form.city || null,
      address: editCenter.form.address || null,
      description: editCenter.form.description || null,
    };

    const { data } = await api.patch(`${ENDPOINTS.centers}${editCenter.id}/`, payload);

    const idx = centers.value.findIndex((x) => x.id === editCenter.id);
    if (idx !== -1) centers.value[idx] = data;

    closeEditCenter();
  } catch (e: any) {
    globalError.value = normalizeApiError(e);
  } finally {
    editCenter.saving = false;
  }
}

/* ------------------------- EDIT PROGRAM ------------------------- */
const editProgram = reactive<{
  open: boolean;
  id: number | null;
  saving: boolean;
  form: {
    center_id: number | null;
    title: string;
    description: string;
    category_id: number | null;
    topic: string;
    format: ProgramFormat;
    price: number | null;
    currency: string;
    schedule: string;
    age_min: number | null;
    age_max: number | null;
    is_active: boolean;
  };
}>({
  open: false,
  id: null,
  saving: false,
  form: {
    center_id: null,
    title: "",
    description: "",
    category_id: null,
    topic: "",
    format: "OFFLINE",
    price: null,
    currency: "KGS",
    schedule: "",
    age_min: null,
    age_max: null,
    is_active: true,
  },
});

function openEditProgram(p: Program) {
  editProgram.open = true;
  editProgram.id = p.id;

  editProgram.form.center_id = p.center?.id ?? null;
  editProgram.form.title = p.title ?? "";
  editProgram.form.description = (p.description ?? "") as string;
  editProgram.form.category_id = p.category?.id ?? null;
  editProgram.form.topic = (p.topic ?? "") as string;
  editProgram.form.format = p.format ?? "OFFLINE";
  editProgram.form.price = (p.price ?? null) as number | null;
  editProgram.form.currency = p.currency ?? "KGS";
  editProgram.form.schedule = (p.schedule ?? "") as string;
  editProgram.form.age_min = (p.age_min ?? null) as number | null;
  editProgram.form.age_max = (p.age_max ?? null) as number | null;
  editProgram.form.is_active = !!p.is_active;
}

function closeEditProgram() {
  if (editProgram.saving) return;
  editProgram.open = false;
  editProgram.id = null;
}

async function saveEditProgram() {
  if (!editProgram.id) return;
  editProgram.saving = true;
  globalError.value = null;

  try {
    if (!editProgram.form.center_id) throw new Error("Выберите центр.");
    if (!editProgram.form.category_id) throw new Error("Выберите категорию.");

    const payload = {
      title: editProgram.form.title,
      description: editProgram.form.description,
      topic: editProgram.form.topic ?? "",
      format: editProgram.form.format,
      price: editProgram.form.price,
      currency: editProgram.form.currency || "KGS",
      schedule: editProgram.form.schedule ?? "",
      age_min: editProgram.form.age_min,
      age_max: editProgram.form.age_max,
      is_active: editProgram.form.is_active,
      center_id: editProgram.form.center_id,
      category_id: editProgram.form.category_id,
    };

    const { data } = await api.patch(`${ENDPOINTS.programs}${editProgram.id}/`, payload);

    const idx = programs.value.findIndex((x) => x.id === editProgram.id);
    if (idx !== -1) programs.value[idx] = data;

    closeEditProgram();
  } catch (e: any) {
    globalError.value = e?.message && !e?.response ? String(e.message) : normalizeApiError(e);
  } finally {
    editProgram.saving = false;
  }
}

onMounted(async () => {
  if (authUser.value && isAdmin.value) await reloadAll();
});
</script>

<style scoped>
.page {
  max-width: 1200px;
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
.page__header { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom:18px; }
.title { font-size:30px; line-height:1.15; margin:0; letter-spacing:-0.02em; color:#eef2ff; }
.subtitle { margin:10px 0 0; color:rgba(226,232,240,0.75); }
.page__meta { display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
.chip {
  border:1px solid rgba(148,163,184,0.25);
  background:rgba(15,23,42,0.65);
  color:#e2e8f0;
  padding:8px 10px;
  border-radius:999px;
  font-size:13px;
  backdrop-filter: blur(8px);
}

.grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.grid__span2 { grid-column: span 2; }

.card {
  border:1px solid rgba(148,163,184,0.18);
  background:rgba(255,255,255,0.98);
  border-radius:16px;
  padding:16px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.35), 0 2px 10px rgba(0,0,0,0.18);
}
.card__head { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:12px; }
.card__title { margin:0; font-size:18px; font-weight:700; color:#0f172a; }

.form { display:grid; gap:12px; margin-top:10px; }
.form--grid { grid-template-columns: 1.2fr 1fr 0.6fr; }
.form__row { display:grid; gap:6px; }
.form__row--full { grid-column: span 3; }
.form__actions { display:flex; gap:10px; align-items:center; }
.form__actions--full { grid-column: span 3; }

.label { font-size:13px; font-weight:600; color:#334155; }

.input, .textarea, .select {
  width:100%;
  border:1px solid #d7deea;
  border-radius:12px;
  padding:10px 12px;
  outline:none;
  background:#fff;
  font-size:14px;
  color:#0f172a;
  transition: box-shadow .15s ease, border-color .15s ease, transform .05s ease;
}
.textarea { min-height:96px; resize:vertical; line-height:1.35; }
.input:focus, .textarea:focus, .select:focus { border-color: rgba(37,99,235,0.7); box-shadow: 0 0 0 4px rgba(37,99,235,0.15); }

.select {
  appearance:none;
  background-image:
    linear-gradient(45deg, transparent 50%, rgba(15,23,42,.6) 50%),
    linear-gradient(135deg, rgba(15,23,42,.6) 50%, transparent 50%),
    linear-gradient(to right, transparent, transparent);
  background-position:
    calc(100% - 18px) calc(1em + 2px),
    calc(100% - 13px) calc(1em + 2px),
    100% 0;
  background-size: 5px 5px, 5px 5px, 2.5em 2.5em;
  background-repeat:no-repeat;
}

.btn {
  border:1px solid rgba(148,163,184,0.5);
  background:#fff;
  padding:10px 14px;
  border-radius:12px;
  cursor:pointer;
  font-size:14px;
  font-weight:600;
  color:#0f172a;
  transition: transform .05s ease, box-shadow .15s ease, background .15s ease, border-color .15s ease;
}
.btn:hover { box-shadow: 0 8px 22px rgba(15,23,42,0.10); }
.btn:active { transform: translateY(1px); }
.btn:disabled { opacity:0.55; cursor:not-allowed; box-shadow:none; }

.btn--primary { border-color: rgba(37,99,235,0.8); background: linear-gradient(180deg,#2563eb 0%, #1d4ed8 100%); color:#fff; }
.btn--danger { border-color: rgba(239,68,68,0.85); background: linear-gradient(180deg,#ef4444 0%, #dc2626 100%); color:#fff; }
.btn--ghost { background:#f1f5f9; border-color: rgba(148,163,184,0.35); color:#0f172a; }

.divider { height:1px; background:#e8eef7; margin:14px 0; }

.list { display:grid; gap:10px; }
.list__head { display:flex; justify-content:space-between; align-items:center; }

.item {
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:12px;
  border:1px solid #edf2f8;
  background:#fbfdff;
  border-radius:14px;
  padding:12px 12px;
}
.item__main { min-width:0; }
.item__title { font-weight:800; color:#0f172a; line-height:1.25; }
.item__meta {
  margin-top:6px;
  color:#475569;
  font-size:13px;
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  line-height:1.35;
  overflow-wrap:anywhere;
  word-break: break-word;
}
.item__actions { display:flex; align-items:center; gap:10px; }
.actions-col { flex-direction: column; align-items: stretch; }

.muted { color:#64748b; font-size:13px; }

.alert { border-radius:14px; padding:12px 12px; border:1px solid; font-weight:600; }
.alert--warning { background:#fff7e6; border-color:#ffd591; color:#874d00; }
.alert--danger { background:#fff1f2; border-color:#fecdd3; color:#7f1d1d; }

.program-meta { display:grid; gap:6px; }
.meta-row { display:flex; gap:6px; align-items:baseline; font-size:13px; }
.meta-label { font-weight:600; color:#334155; min-width:90px; }
.meta-value { color:#0f172a; }
.meta-muted { color:#64748b; font-size:12px; }
.meta-price { font-weight:700; color:#1d4ed8; }

.checkbox-row { display:flex; align-items:center; gap:10px; }

@media (max-width: 980px) {
  .grid { grid-template-columns: 1fr; }
  .grid__span2 { grid-column: span 1; }
  .form--grid { grid-template-columns: 1fr; }
  .form__row--full, .form__actions--full { grid-column: span 1; }
  .page__header { flex-direction: column; }
  .actions-col { flex-direction: row; }
}

/* Modal */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.65);
  display: grid;
  place-items: center;
  padding: 18px;
  z-index: 50;
}
.modal__card {
  width: min(980px, 100%);
  background: rgba(255,255,255,0.98);
  border: 1px solid rgba(148,163,184,0.25);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.45);
}
.modal__head {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
  margin-bottom: 10px;
}
.modal__title { margin:0; font-size: 18px; font-weight: 800; color:#0f172a; }
/* Сетка карточек программ: 2 в ряд на обычных экранах */
.programs-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

/* Чтобы карточка не разъезжалась по высоте */
.program-item {
  height: 100%;
}

/* На узких экранах — 1 в ряд */
@media (max-width: 980px) {
  .programs-grid {
    grid-template-columns: 1fr;
  }
}
.checkbox {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: #0f172a;
}
.checkbox input {
  width: 16px;
  height: 16px;
}
.modalOverlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.55);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 16px;
}

.modal {
  width: min(720px, 100%);
  background: #fff;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 18px 60px rgba(0,0,0,.25);
  border: 1px solid rgba(17,24,39,.12);
}

.modal--wide {
  width: min(860px, 100%);
}

.modalTitle {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 900;
  color: #111;
}

.modalActions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.checkbox {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: #0f172a;
}
.checkbox input {
  width: 16px;
  height: 16px;
}

</style>
