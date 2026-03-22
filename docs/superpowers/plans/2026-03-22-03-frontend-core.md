# FlashCards — Plán 3: Frontend core

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Funkční Vue.js SPA — Dashboard se stromem jazyků/lekcí a kompletní učební session s SM-2 animacemi, undo, session persistence.

**Architecture:** Vue.js 3 Composition API + Vite. Pinia store per doménová entita. Vue Router pro navigaci. Axios pro API volání. Tailwind CSS pro styling. Komponenty jsou malé a jednopříčelové — žádné "mega-komponenty".

**Tech Stack:** Vue.js 3, Vite, Pinia, Vue Router 4, Axios, Tailwind CSS

**Předpoklady:** Plán 2 dokončen — backend API běží na `http://localhost/api`.

---

## Struktura souborů

```
frontend/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── index.html
└── src/
    ├── main.js
    ├── router.js
    ├── api.js                    # Axios instance + všechna API volání
    ├── stores/
    │   ├── languages.js          # Pinia store pro jazyky + lekce
    │   └── study.js              # Pinia store pro study session
    ├── components/
    │   ├── layout/
    │   │   ├── AppSidebar.vue    # Desktop sidebar s hierarchií
    │   │   ├── AppTopbar.vue     # Mobilní top bar
    │   │   └── AppLayout.vue     # Wrapper — sidebar/topbar dle viewportu
    │   ├── sidebar/
    │   │   ├── LanguageItem.vue  # Jazyk s lekcemi v stromu
    │   │   ├── LessonItem.vue    # Lekce s checkboxem + počty
    │   │   └── ContextMenu.vue   # ⋯ menu (přejmenovat/reset/smazat)
    │   └── study/
    │       ├── StudyCard.vue     # Karta (přední/zadní, animace)
    │       ├── RatingButtons.vue # 4 hodnoticí tlačítka
    │       └── UndoButton.vue    # Tlačítko Zpět
    └── views/
        ├── DashboardView.vue     # Hlavní obrazovka (wrapper + welcome)
        └── StudyView.vue         # Učební session
```

---

## Task 1: Vite + Vue projekt

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`

- [ ] **Step 1: Inicializuj projekt**

```bash
mkdir frontend && cd frontend
npm create vite@latest . -- --template vue
npm install
npm install pinia vue-router@4 axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

- [ ] **Step 2: Uprav `tailwind.config.js`**

```js
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: { extend: {} },
  plugins: [],
}
```

- [ ] **Step 3: Přidej Tailwind do `src/style.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 4: Uprav `vite.config.js`** — proxy API na backend

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    }
  }
})
```

- [ ] **Step 5: Uprav `src/main.js`**

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

createApp(App).use(createPinia()).use(router).mount('#app')
```

- [ ] **Step 6: Vytvoř `src/router.js`**

```js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from './views/DashboardView.vue'
import StudyView from './views/StudyView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardView },
    { path: '/study', component: StudyView },
  ]
})
```

- [ ] **Step 7: Ověř že projekt startuje**

```bash
npm run dev
# Otevři http://localhost:5173
```

- [ ] **Step 8: Commit**

```bash
git add frontend/
git commit -m "feat: vue3 + vite + pinia + tailwind setup"
```

---

## Task 2: API vrstva

**Files:**
- Create: `frontend/src/api.js`

- [ ] **Step 1: Vytvoř `frontend/src/api.js`**

```js
import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export const api = {
  // Dashboard
  getDashboard: () => http.get('/dashboard'),

  // Languages
  getLanguages: () => http.get('/languages'),
  createLanguage: (data) => http.post('/languages', data),
  updateLanguage: (id, data) => http.patch(`/languages/${id}`, data),
  deleteLanguage: (id) => http.delete(`/languages/${id}`),

  // Lessons
  getLessons: (languageId) => http.get('/lessons', { params: { language_id: languageId } }),
  createLesson: (data) => http.post('/lessons', data),
  updateLesson: (id, data) => http.patch(`/lessons/${id}`, data),
  deleteLesson: (id) => http.delete(`/lessons/${id}`),

  // Cards
  getCards: (lessonId) => http.get('/cards', { params: { lesson_id: lessonId } }),
  createCard: (data) => http.post('/cards', data),
  updateCard: (id, data) => http.patch(`/cards/${id}`, data),
  deleteCard: (id) => http.delete(`/cards/${id}`),

  // Study
  getStudyCards: (lessonIds) => http.post('/study/cards', { lesson_ids: lessonIds }),
  rateCard: (data) => http.post('/study/rate', data),
  undoRating: (previousState) => http.post('/study/undo', previousState),

  // Import
  importCards: (lessonId, file) => {
    const form = new FormData()
    form.append('lesson_id', lessonId)
    form.append('file', file)
    return http.post('/import', form)
  },

  // Translate
  translate: (text, targetLang) => http.post('/translate', { text, target_lang: targetLang }),
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api.js
git commit -m "feat: api layer"
```

---

## Task 3: Pinia stores

**Files:**
- Create: `frontend/src/stores/languages.js`
- Create: `frontend/src/stores/study.js`

- [ ] **Step 1: Vytvoř `frontend/src/stores/languages.js`**

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api'

export const useLanguagesStore = defineStore('languages', () => {
  const languages = ref([])
  const selectedLessonIds = ref(new Set())

  async function fetchDashboard() {
    const { data } = await api.getDashboard()
    languages.value = data
  }

  function toggleLesson(lessonId) {
    if (selectedLessonIds.value.has(lessonId)) {
      selectedLessonIds.value.delete(lessonId)
    } else {
      selectedLessonIds.value.add(lessonId)
    }
  }

  const selectedCount = computed(() => selectedLessonIds.value.size)

  async function deleteLanguage(id) {
    await api.deleteLanguage(id)
    await fetchDashboard()
  }

  async function deleteLesson(id) {
    await api.deleteLesson(id)
    selectedLessonIds.value.delete(id)
    await fetchDashboard()
  }

  return { languages, selectedLessonIds, selectedCount, fetchDashboard, toggleLesson, deleteLanguage, deleteLesson }
})
```

- [ ] **Step 2: Vytvoř `frontend/src/stores/study.js`**

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api'

const SESSION_KEY = 'flashcards_session'

export const useStudyStore = defineStore('study', () => {
  const cards = ref([])
  const currentIndex = ref(0)
  const history = ref([])  // [{card, rating, previousState}] — max 5 položek
  const revealed = ref(false)
  const animationDirection = ref(null)  // 'left' | 'right' | null

  const currentCard = computed(() => cards.value[currentIndex.value] ?? null)
  const isFinished = computed(() => currentIndex.value >= cards.value.length)

  async function startSession(lessonIds) {
    const { data } = await api.getStudyCards(lessonIds)
    cards.value = data
    currentIndex.value = 0
    history.value = []
    revealed.value = false
    saveSession(lessonIds)
  }

  function saveSession(lessonIds) {
    localStorage.setItem(SESSION_KEY, JSON.stringify({
      lessonIds,
      cardIds: cards.value.map(c => c.card_id),
      currentIndex: currentIndex.value,
    }))
  }

  function loadSavedSession() {
    const raw = localStorage.getItem(SESSION_KEY)
    return raw ? JSON.parse(raw) : null
  }

  function clearSession() {
    localStorage.removeItem(SESSION_KEY)
  }

  function reveal() {
    revealed.value = true
  }

  async function rate(quality) {
    const card = currentCard.value
    if (!card) return

    animationDirection.value = quality < 3 ? 'left' : 'right'

    const { data } = await api.rateCard({
      card_id: card.card_id,
      direction: card.direction,
      quality,
    })

    // Ulož do history pro undo
    history.value = [
      { card, quality, previousState: data.previous_state },
      ...history.value,
    ].slice(0, 5)

    setTimeout(() => {
      currentIndex.value++
      revealed.value = false
      animationDirection.value = null
      saveSession(null)  // aktualizuj index
    }, 300)  // počkej na animaci
  }

  async function undo() {
    if (history.value.length === 0) return
    const last = history.value.shift()
    await api.undoRating(last.previousState)
    currentIndex.value--
    revealed.value = false
  }

  return {
    cards, currentIndex, history, revealed, animationDirection,
    currentCard, isFinished,
    startSession, loadSavedSession, clearSession, reveal, rate, undo,
  }
})
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/stores/
git commit -m "feat: pinia stores for languages and study session"
```

---

## Task 4: Layout komponenty

**Files:**
- Create: `frontend/src/components/layout/AppLayout.vue`
- Create: `frontend/src/components/layout/AppSidebar.vue`
- Create: `frontend/src/components/layout/AppTopbar.vue`

- [ ] **Step 1: Vytvoř `AppLayout.vue`** — přepíná sidebar/topbar dle viewportu

```vue
<template>
  <div class="flex h-screen bg-gray-950 text-gray-100">
    <!-- Desktop sidebar -->
    <AppSidebar v-if="!isMobile" />

    <!-- Mobilní overlay menu -->
    <div v-if="isMobile && menuOpen" class="fixed inset-0 z-40 flex">
      <div class="w-72 bg-gray-900 h-full overflow-y-auto">
        <AppSidebar @close="menuOpen = false" />
      </div>
      <div class="flex-1 bg-black/50" @click="menuOpen = false" />
    </div>

    <div class="flex flex-col flex-1 overflow-hidden">
      <AppTopbar v-if="isMobile" @menu="menuOpen = true" />
      <main class="flex-1 overflow-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'

const isMobile = ref(false)
const menuOpen = ref(false)

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => { checkMobile(); window.addEventListener('resize', checkMobile) })
onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>
```

- [ ] **Step 2: Vytvoř `AppSidebar.vue`**

```vue
<template>
  <aside class="w-[180px] bg-gray-900 flex flex-col border-r border-gray-800 shrink-0">
    <!-- Header -->
    <div class="p-3 border-b border-gray-800 flex items-center justify-between">
      <span class="text-indigo-400 font-bold text-sm">📚 FlashCards</span>
      <span class="w-6 h-6 rounded-full bg-gray-700 flex items-center justify-center text-xs">👤</span>
    </div>

    <!-- Language tree -->
    <div class="flex-1 overflow-y-auto p-2 space-y-1">
      <LanguageItem
        v-for="lang in store.languages"
        :key="lang.id"
        :language="lang"
      />
    </div>

    <!-- Start button -->
    <div class="p-2 border-t border-gray-800">
      <button
        v-if="store.selectedCount > 0"
        @click="startStudy"
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold py-2 rounded-lg"
      >
        ▶ Začít vybrané ({{ store.selectedCount }})
      </button>
    </div>

    <!-- Nav -->
    <div class="p-2 border-t border-gray-800 text-xs space-y-1">
      <router-link to="/stats" class="block px-2 py-1 text-gray-400 hover:text-white rounded">📊 Statistiky</router-link>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useLanguagesStore } from '../../stores/languages'
import LanguageItem from '../sidebar/LanguageItem.vue'

const store = useLanguagesStore()
const router = useRouter()

function startStudy() {
  router.push({ path: '/study', query: { lessons: [...store.selectedLessonIds].join(',') } })
}
</script>
```

- [ ] **Step 3: Vytvoř `AppTopbar.vue`** — mobilní top bar

```vue
<template>
  <header class="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between">
    <button @click="$emit('menu')" class="text-gray-400 text-xl">☰</button>
    <span class="text-indigo-400 font-bold text-sm">FlashCards</span>
    <span class="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-xs">👤</span>
  </header>
</template>

<script setup>
defineEmits(['menu'])
</script>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/layout/
git commit -m "feat: app layout with sidebar and mobile topbar"
```

---

## Task 5: Sidebar komponenty — LanguageItem + LessonItem + ContextMenu

**Files:**
- Create: `frontend/src/components/sidebar/LanguageItem.vue`
- Create: `frontend/src/components/sidebar/LessonItem.vue`
- Create: `frontend/src/components/sidebar/ContextMenu.vue`

- [ ] **Step 1: Vytvoř `LessonItem.vue`**

```vue
<template>
  <div class="flex items-center gap-1 px-2 py-1 rounded text-xs cursor-pointer hover:bg-gray-800"
       :class="isSelected ? 'bg-indigo-950' : ''">
    <input type="checkbox" :checked="isSelected" @change="store.toggleLesson(lesson.id)"
           class="accent-indigo-500 w-3 h-3" />
    <span class="flex-1 truncate" :class="isSelected ? 'text-indigo-200' : 'text-gray-400'">
      {{ lesson.name }}
    </span>
    <span class="text-green-400 font-bold">{{ lesson.learned_cards }}</span>
    <span class="text-gray-600">/{{ lesson.total_cards }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguagesStore } from '../../stores/languages'

const props = defineProps({ lesson: Object })
const store = useLanguagesStore()
const isSelected = computed(() => store.selectedLessonIds.has(props.lesson.id))
</script>
```

- [ ] **Step 2: Vytvoř `LanguageItem.vue`**

```vue
<template>
  <div>
    <div class="flex items-center gap-1 px-2 py-1 rounded cursor-pointer hover:bg-gray-800"
         @click="expanded = !expanded">
      <span class="text-gray-500 text-xs">{{ expanded ? '▼' : '▶' }}</span>
      <span class="text-sm">{{ language.emoji }}</span>
      <span class="flex-1 text-xs font-semibold text-gray-200 truncate">{{ language.name }}</span>
      <span class="text-green-400 text-xs font-bold">{{ language.learned_cards }}</span>
      <span class="text-gray-600 text-xs">/{{ language.total_cards }}</span>
    </div>
    <div v-if="expanded" class="pl-4 space-y-0.5">
      <LessonItem v-for="lesson in language.lessons" :key="lesson.id" :lesson="lesson" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LessonItem from './LessonItem.vue'

defineProps({ language: Object })
const expanded = ref(true)
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/sidebar/
git commit -m "feat: sidebar language/lesson tree with checkboxes"
```

---

## Task 6: Study komponenty — karta s animací

**Files:**
- Create: `frontend/src/components/study/StudyCard.vue`
- Create: `frontend/src/components/study/RatingButtons.vue`
- Create: `frontend/src/components/study/UndoButton.vue`

- [ ] **Step 1: Vytvoř `StudyCard.vue`** — karta s flip animací a slide-out

```vue
<template>
  <div class="relative flex items-center justify-center">
    <!-- Slide-out animace -->
    <Transition :name="slideClass" mode="out-in">
      <div
        :key="card.card_id + card.direction"
        class="bg-gradient-to-br from-indigo-950 to-gray-900 border border-indigo-800 rounded-2xl p-8 text-center w-80 cursor-pointer select-none"
        @click="!revealed && emit('reveal')"
      >
        <p class="text-indigo-300 text-xs uppercase tracking-widest mb-4">
          {{ card.direction === 'front_to_back' ? 'Přelož' : 'Co to je?' }}
        </p>
        <p class="text-white text-3xl font-bold mb-4">{{ card.front }}</p>

        <!-- Audio přední strany -->
        <button v-if="card.front_audio" @click.stop="playAudio(card.front_audio)"
                class="text-indigo-400 text-sm mb-4">🔊 přehrát</button>

        <!-- Zadní strana — po odkrytí -->
        <Transition name="fade">
          <div v-if="revealed" class="mt-4 border-t border-indigo-800 pt-4">
            <p class="text-gray-300 text-2xl">{{ card.back }}</p>
            <img v-if="card.back_image" :src="`/media/${card.back_image}`"
                 class="mt-3 rounded-lg max-h-32 mx-auto" />
            <button v-if="card.back_audio" @click.stop="playAudio(card.back_audio)"
                    class="text-indigo-400 text-sm mt-2">🔊</button>
          </div>
        </Transition>

        <p v-if="!revealed" class="text-gray-600 text-xs mt-6">klikni pro odhalení</p>
      </div>
    </Transition>
  </div>
</template>

<script setup>
defineProps({ card: Object, revealed: Boolean, slideClass: String })
const emit = defineEmits(['reveal'])

function playAudio(path) {
  new Audio(`/media/${path}`).play()
}
</script>

<style scoped>
.slide-left-enter-active, .slide-left-leave-active,
.slide-right-enter-active, .slide-right-leave-active { transition: all 0.3s ease; }
.slide-left-leave-to { transform: translateX(-100%); opacity: 0; }
.slide-right-leave-to { transform: translateX(100%); opacity: 0; }
.slide-left-enter-from, .slide-right-enter-from { transform: translateX(0); opacity: 1; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
```

- [ ] **Step 2: Vytvoř `RatingButtons.vue`**

```vue
<template>
  <div class="flex gap-3 justify-center">
    <button @click="$emit('rate', 0)" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-semibold">✗ Nevím</button>
    <button @click="$emit('rate', 3)" class="bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">~ Těžké</button>
    <button @click="$emit('rate', 4)" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold">✓ Umím</button>
    <button @click="$emit('rate', 5)" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold">⚡ Lehké</button>
  </div>
</template>

<script setup>
defineEmits(['rate'])
</script>
```

- [ ] **Step 3: Vytvoř `UndoButton.vue`**

```vue
<template>
  <button
    v-if="canUndo"
    @click="$emit('undo')"
    class="text-gray-500 hover:text-gray-300 text-xs flex items-center gap-1"
  >
    ↩ Zpět
  </button>
</template>

<script setup>
defineProps({ canUndo: Boolean })
defineEmits(['undo'])
</script>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/study/
git commit -m "feat: study card component with flip animation and rating buttons"
```

---

## Task 7: DashboardView + StudyView

**Files:**
- Create: `frontend/src/views/DashboardView.vue`
- Create: `frontend/src/views/StudyView.vue`
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Vytvoř `DashboardView.vue`**

```vue
<template>
  <AppLayout>
    <div class="flex items-center justify-center h-full text-gray-600 text-sm">
      <div class="text-center">
        <p class="text-4xl mb-4">📚</p>
        <p>Vyber lekce v postranním panelu a klikni Začít.</p>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import { useLanguagesStore } from '../stores/languages'
import AppLayout from '../components/layout/AppLayout.vue'

const store = useLanguagesStore()
onMounted(() => store.fetchDashboard())
</script>
```

- [ ] **Step 2: Vytvoř `StudyView.vue`**

```vue
<template>
  <AppLayout>
    <div class="flex flex-col items-center justify-center h-full gap-6 p-4">

      <!-- Session recovery dialog -->
      <div v-if="showRecovery" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="bg-gray-900 rounded-xl p-6 text-center space-y-4">
          <p class="text-white font-semibold">Máš rozdělanou session. Pokračovat?</p>
          <div class="flex gap-3 justify-center">
            <button @click="resumeSession" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Pokračovat</button>
            <button @click="discardSession" class="bg-gray-700 text-white px-4 py-2 rounded-lg text-sm">Začít znovu</button>
          </div>
        </div>
      </div>

      <!-- Progress + Undo -->
      <div class="flex items-center justify-between w-80">
        <span class="text-gray-500 text-xs">{{ store.currentIndex }} / {{ store.cards.length }}</span>
        <UndoButton :can-undo="store.history.length > 0" @undo="store.undo()" />
      </div>

      <!-- Progress bar -->
      <div class="w-80 bg-gray-800 rounded-full h-1">
        <div class="bg-indigo-500 h-1 rounded-full transition-all"
             :style="{ width: `${(store.currentIndex / store.cards.length) * 100}%` }" />
      </div>

      <!-- Karta nebo finish -->
      <template v-if="!store.isFinished && store.currentCard">
        <StudyCard
          :card="store.currentCard"
          :revealed="store.revealed"
          :slide-class="slideClass"
          @reveal="store.reveal()"
        />
        <RatingButtons v-if="store.revealed" @rate="handleRate" />
        <p v-else class="text-gray-600 text-xs">Klikni na kartu pro odhalení</p>
      </template>

      <div v-else-if="store.isFinished" class="text-center space-y-4">
        <p class="text-4xl">🎉</p>
        <p class="text-white font-semibold">Session dokončena!</p>
        <button @click="$router.push('/')" class="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm">
          Zpět na Dashboard
        </button>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStudyStore } from '../stores/study'
import AppLayout from '../components/layout/AppLayout.vue'
import StudyCard from '../components/study/StudyCard.vue'
import RatingButtons from '../components/study/RatingButtons.vue'
import UndoButton from '../components/study/UndoButton.vue'

const route = useRoute()
const router = useRouter()
const store = useStudyStore()
const showRecovery = ref(false)
const slideClass = computed(() =>
  store.animationDirection === 'left' ? 'slide-left' : 'slide-right'
)

onMounted(async () => {
  const lessonParam = route.query.lessons
  const saved = store.loadSavedSession()

  if (saved && !lessonParam) {
    showRecovery.value = true
    return
  }

  if (lessonParam) {
    const lessonIds = lessonParam.split(',')
    await store.startSession(lessonIds)
  }
})

async function resumeSession() {
  showRecovery.value = false
  // Obnov session ze saved state — znovu fetch karet, přejdi na uloženou pozici
  const saved = store.loadSavedSession()
  await store.startSession(saved.lessonIds)
  store.currentIndex = saved.currentIndex
}

function discardSession() {
  store.clearSession()
  showRecovery.value = false
  router.push('/')
}

async function handleRate(quality) {
  await store.rate(quality)
}
</script>
```

- [ ] **Step 3: Uprav `App.vue`** — jen RouterView

```vue
<template>
  <RouterView />
</template>
```

- [ ] **Step 4: Ověř v prohlížeči**

```bash
cd frontend && npm run dev
# http://localhost:5173 — Dashboard se stromem jazyků
# Vyber lekce → Začít → Study session s kartami a animacemi
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/ frontend/src/App.vue
git commit -m "feat: dashboard and study views with session persistence"
```

---

## Task 8: MediaUpload komponenta

**Files:**
- Create: `frontend/src/components/cards/MediaUpload.vue`

- [ ] **Step 1: Vytvoř `MediaUpload.vue`**

```vue
<template>
  <div class="flex items-center gap-2">
    <input ref="fileInput" type="file" :accept="acceptTypes" class="hidden" @change="handleFile" />
    <button
      type="button"
      @click="fileInput.click()"
      class="text-xs text-gray-500 hover:text-gray-300 border border-gray-700 rounded px-2 py-1"
    >
      {{ currentPath ? '🔄 Změnit' : '📎 Přidat' }} {{ label === 'front' ? 'přední' : 'zadní' }} media
    </button>
    <span v-if="currentPath" class="text-xs text-gray-600 truncate max-w-32">{{ fileName }}</span>
    <button v-if="currentPath" @click="remove" class="text-xs text-red-600 hover:text-red-400">✕</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { api } from '../../api'

const props = defineProps({
  cardId: String,
  label: String,
  modelValue: String,  // current path
})
const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const acceptTypes = 'image/png,image/jpeg,image/webp,audio/mpeg,audio/ogg'
const currentPath = computed(() => props.modelValue)
const fileName = computed(() => currentPath.value?.split('/').pop() ?? '')

async function handleFile(e) {
  const file = e.target.files[0]
  if (!file || !props.cardId) return
  const { data } = await api.uploadMedia(props.cardId, props.label, file)
  emit('update:modelValue', data.path)
}

function remove() {
  emit('update:modelValue', null)
}
</script>
```

- [ ] **Step 2: Přidej `uploadMedia` do `api.js`**

```js
uploadMedia: (cardId, label, file) => {
  const form = new FormData()
  form.append('file', file)
  return http.post(`/cards/${cardId}/media/${label}`, form)
},
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/cards/MediaUpload.vue frontend/src/api.js
git commit -m "feat: media upload component"
```

---

## Task 9: Nginx Dockerfile pro frontend

**Files:**
- Modify: `nginx/Dockerfile`
- Create: `frontend/Dockerfile`

- [ ] **Step 1: Vytvoř `frontend/Dockerfile`**

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

- [ ] **Step 2: Uprav `docker-compose.yml`** — nginx zkopíruje statické soubory z frontend image

```yaml
  nginx:
    build:
      context: .
      dockerfile: nginx/Dockerfile
    # nebo použij multi-stage s frontend buildem
```

Jednodušší alternativa: nginx image buildí frontend i kopíruje config v jednom:

```dockerfile
# nginx/Dockerfile
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
```

- [ ] **Step 3: Otestuj Docker build**

```bash
docker compose build nginx
docker compose up
# http://localhost — kompletní app přes Docker
```

- [ ] **Step 4: Commit**

```bash
git add frontend/Dockerfile nginx/Dockerfile docker-compose.yml
git commit -m "feat: frontend docker build with nginx"
```

---

## Hotovo

Na konci tohoto plánu:
- ✅ Vue.js SPA s Pinia + Vue Router
- ✅ Dashboard se stromem jazyků/lekcí, checkboxy, "Začít vybrané"
- ✅ Study session — karta, odhalení, animace, 4 hodnoticí tlačítka
- ✅ Tlačítko Zpět (undo, max 5 kroků)
- ✅ Session persistence v localStorage + recovery dialog
- ✅ Responzivní layout — sidebar na desktopu, hamburger na mobilu
- ✅ Frontend buildován přes Docker/Nginx

**Pokračuj plánem 4: Frontend doplňky** (`2026-03-22-04-frontend-features.md`)
