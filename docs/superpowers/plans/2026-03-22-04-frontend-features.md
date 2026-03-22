# FlashCards — Plán 4: Frontend doplňky

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dokončení aplikace — editor karet s auto-překladem, seznam karet, import CSV/JSON, statistiky, kontextová menu (přejmenovat/reset/smazat), správa jazyků a lekcí.

**Architecture:** Nové Vue komponenty a views, napojené na existující API vrstvu a Pinia stores. Žádné nové backend změny.

**Tech Stack:** Vue.js 3, Pinia, Axios (vše z Plánu 3)

**Předpoklady:** Plán 3 dokončen — Dashboard a Study session funkční.

---

## Struktura souborů

```
frontend/src/
├── components/
│   ├── sidebar/
│   │   └── ContextMenu.vue          # ⋯ menu pro jazyk/lekci
│   ├── cards/
│   │   ├── CardList.vue             # Tabulkový seznam karet lekce
│   │   └── CardEditor.vue           # Editor jedné karty (modal nebo stránka)
│   ├── modals/
│   │   ├── ConfirmDialog.vue        # Potvrzovací dialog (smazat/reset)
│   │   ├── RenameDialog.vue         # Dialog pro přejmenování
│   │   └── ImportDialog.vue         # Drag & drop import
│   └── stats/
│       └── StatsChart.vue           # Graf přesnosti
└── views/
    ├── CardListView.vue              # Seznam karet lekce
    ├── CardEditorView.vue            # Editor karty
    ├── ImportView.vue                # Import obrazovka
    └── StatsView.vue                 # Statistiky
```

---

## Task 1: Kontextová menu — přejmenovat, reset, smazat

**Files:**
- Create: `frontend/src/components/sidebar/ContextMenu.vue`
- Create: `frontend/src/components/modals/ConfirmDialog.vue`
- Create: `frontend/src/components/modals/RenameDialog.vue`
- Modify: `frontend/src/components/sidebar/LanguageItem.vue`
- Modify: `frontend/src/components/sidebar/LessonItem.vue`

- [ ] **Step 1: Vytvoř `ConfirmDialog.vue`**

```vue
<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">{{ title }}</p>
        <p class="text-gray-400 text-sm">{{ message }}</p>
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="$emit('confirm')" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm">
            {{ confirmLabel }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({ title: String, message: String, confirmLabel: { type: String, default: 'Smazat' } })
defineEmits(['confirm', 'cancel'])
</script>
```

- [ ] **Step 2: Vytvoř `RenameDialog.vue`**

```vue
<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">Přejmenovat</p>
        <input
          v-model="value"
          @keyup.enter="$emit('confirm', value)"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500"
          autofocus
        />
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="$emit('confirm', value)" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Uložit</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ initialValue: String })
defineEmits(['confirm', 'cancel'])
const value = ref(props.initialValue || '')
</script>
```

- [ ] **Step 3: Vytvoř `ContextMenu.vue`**

```vue
<template>
  <div class="relative">
    <button @click.stop="open = !open" class="text-gray-600 hover:text-gray-300 px-1">⋯</button>
    <div v-if="open" class="absolute right-0 top-5 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-30 w-36 py-1 text-xs">
      <button @click="emit('rename'); open = false" class="w-full text-left px-3 py-2 hover:bg-gray-700 text-gray-300">✏️ Přejmenovat</button>
      <button v-if="showReset" @click="emit('reset'); open = false" class="w-full text-left px-3 py-2 hover:bg-gray-700 text-gray-300">🔄 Reset progressu</button>
      <button @click="emit('delete'); open = false" class="w-full text-left px-3 py-2 hover:bg-red-900 text-red-400">🗑 Smazat</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ showReset: { type: Boolean, default: true } })
const emit = defineEmits(['rename', 'reset', 'delete'])
const open = ref(false)
</script>
```

- [ ] **Step 4: Přidej ContextMenu do `LanguageItem.vue` a `LessonItem.vue`**

Do `LanguageItem.vue` přidej:
- `<ContextMenu>` vedle názvu jazyka
- handlery pro rename/reset/delete — volají store metody
- `<RenameDialog>` a `<ConfirmDialog>` při příslušné akci

Příklad handleru:
```js
async function handleDelete() {
  showConfirm.value = false
  await store.deleteLanguage(language.id)
}

async function handleReset() {
  await api.resetProgress(language.id)  // přidej endpoint do api.js
  await store.fetchDashboard()
}
```

Přidej reset progress endpoint do backendu (`DELETE /api/languages/{id}/progress`) a do `api.js`.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/
git commit -m "feat: context menus with rename, reset, delete dialogs"
```

---

## Task 2: Správa jazyků a lekcí — formuláře pro přidání

**Files:**
- Modify: `frontend/src/components/layout/AppSidebar.vue`

- [ ] **Step 1: Přidej tlačítko "+ Jazyk" do sidebaru**

```vue
<!-- Pod stromem jazyků -->
<button @click="showAddLang = true" class="w-full text-left text-xs text-gray-600 hover:text-gray-400 px-2 py-1">
  + Přidat jazyk
</button>
```

- [ ] **Step 2: Přidej inline formulář pro nový jazyk**

```vue
<div v-if="showAddLang" class="px-2 pb-2 space-y-1">
  <input v-model="newLangName" placeholder="Název jazyka" class="w-full bg-gray-800 rounded px-2 py-1 text-xs text-white" />
  <input v-model="newLangEmoji" placeholder="🏳️" class="w-16 bg-gray-800 rounded px-2 py-1 text-xs text-white" />
  <div class="flex gap-1">
    <button @click="addLanguage" class="bg-indigo-600 text-white text-xs px-2 py-1 rounded flex-1">Přidat</button>
    <button @click="showAddLang = false" class="text-gray-500 text-xs px-2 py-1">Zrušit</button>
  </div>
</div>
```

- [ ] **Step 3: Analogicky přidej "+ Lekce" do `LanguageItem.vue`** — rozbalí se po kliknutí na jazyk

- [ ] **Step 4: Commit**

```bash
git add frontend/src/
git commit -m "feat: add language and lesson forms in sidebar"
```

---

## Task 3: Seznam karet + Editor karty

**Files:**
- Create: `frontend/src/views/CardListView.vue`
- Create: `frontend/src/views/CardEditorView.vue`
- Modify: `frontend/src/router.js`

- [ ] **Step 1: Přidej routes do `router.js`**

```js
{ path: '/lessons/:lessonId/cards', component: () => import('./views/CardListView.vue') },
{ path: '/lessons/:lessonId/cards/new', component: () => import('./views/CardEditorView.vue') },
{ path: '/cards/:cardId/edit', component: () => import('./views/CardEditorView.vue') },
```

- [ ] **Step 2: Vytvoř `CardListView.vue`**

```vue
<template>
  <AppLayout>
    <div class="p-6 max-w-2xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-white font-bold text-lg">{{ lessonName }}</h1>
        <div class="flex gap-2">
          <router-link :to="`/lessons/${lessonId}/import`" class="bg-gray-700 text-white text-xs px-3 py-2 rounded-lg">📥 Import</router-link>
          <router-link :to="`/lessons/${lessonId}/cards/new`" class="bg-indigo-600 text-white text-xs px-3 py-2 rounded-lg">+ Přidat kartu</router-link>
        </div>
      </div>

      <div class="space-y-2">
        <router-link
          v-for="card in cards"
          :key="card.id"
          :to="`/cards/${card.id}/edit`"
          class="flex items-center gap-4 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-lg px-4 py-3"
        >
          <span class="text-white text-sm flex-1">{{ getField(card, 'front') }}</span>
          <span class="text-gray-500 text-sm flex-1">{{ getField(card, 'back') }}</span>
          <span class="text-xs" v-if="getField(card, 'front_image')">🖼</span>
          <span class="text-xs" v-if="getField(card, 'front_audio')">🔊</span>
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const lessonId = route.params.lessonId
const cards = ref([])
const lessonName = ref('')

onMounted(async () => {
  const { data } = await api.getCards(lessonId)
  cards.value = data

  // Načti název lekce z dashboardu
  const { data: dashboard } = await api.getDashboard()
  for (const lang of dashboard) {
    const lesson = lang.lessons.find(l => l.id === lessonId)
    if (lesson) { lessonName.value = lesson.name; break }
  }
})

function getField(card, label) {
  return card.fields.find(f => f.label === label)?.content ?? ''
}
</script>
```

- [ ] **Step 3: Vytvoř `CardEditorView.vue`** — formulář pro novou/existující kartu

```vue
<template>
  <AppLayout>
    <div class="p-6 max-w-lg mx-auto space-y-6">
      <h1 class="text-white font-bold text-lg">{{ isNew ? 'Nová karta' : 'Upravit kartu' }}</h1>

      <!-- Přední strana -->
      <div class="space-y-2">
        <label class="text-gray-400 text-xs uppercase tracking-wider">Přední strana</label>
        <textarea
          v-model="front"
          @input="scheduleTranslate"
          rows="3"
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white text-sm focus:outline-none focus:border-indigo-500 resize-none"
        />
        <!-- Media upload -->
        <MediaUpload :card-id="cardId" label="front" @uploaded="frontImage = $event" />
      </div>

      <!-- Zadní strana -->
      <div class="space-y-2">
        <label class="text-gray-400 text-xs uppercase tracking-wider">Zadní strana</label>
        <textarea
          v-model="back"
          :placeholder="translatePlaceholder"
          rows="3"
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white text-sm focus:outline-none focus:border-indigo-500 resize-none"
          :class="{ 'text-gray-600': isTranslatePlaceholder }"
          @focus="clearTranslatePlaceholder"
        />
        <MediaUpload :card-id="cardId" label="back" @uploaded="backImage = $event" />
      </div>

      <!-- Akce -->
      <div class="flex gap-3">
        <button @click="save" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg text-sm font-semibold flex-1">
          {{ isNew ? 'Přidat kartu' : 'Uložit' }}
        </button>
        <button v-if="!isNew" @click="deleteCard" class="bg-red-900 hover:bg-red-800 text-red-300 px-4 py-2 rounded-lg text-sm">
          Smazat
        </button>
        <button @click="$router.back()" class="text-gray-500 px-4 py-2 text-sm">Zrušit</button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const router = useRouter()
const isNew = computed(() => !route.params.cardId)
const cardId = ref(route.params.cardId || null)
const lessonId = ref(route.params.lessonId)
const front = ref('')
const back = ref('')
const targetLang = ref('cs')  // přepíše se z Language v onMounted
const translatePlaceholder = ref('')
const isTranslatePlaceholder = ref(false)
let translateTimer = null

// Auto-překlad — debounce 1s
async function scheduleTranslate() {
  clearTimeout(translateTimer)
  if (!front.value.trim()) return
  translateTimer = setTimeout(async () => {
    try {
      const { data } = await api.translate(front.value, targetLang.value)
      if (!back.value) {
        back.value = data.translation
      }
    } catch {
      translatePlaceholder.value = 'Překlad není dostupný'
      isTranslatePlaceholder.value = true
    }
  }, 1000)
}

function clearTranslatePlaceholder() {
  if (isTranslatePlaceholder.value) {
    back.value = ''
    translatePlaceholder.value = ''
    isTranslatePlaceholder.value = false
  }
}

async function save() {
  if (isNew.value) {
    await api.createCard({
      lesson_id: lessonId.value,
      fields: [
        { label: 'front', content: front.value },
        { label: 'back', content: back.value },
      ]
    })
  } else {
    await api.updateCard(cardId.value, {
      fields: [
        { label: 'front', content: front.value },
        { label: 'back', content: back.value },
      ]
    })
  }
  router.back()
}

async function deleteCard() {
  if (confirm('Smazat kartu?')) {
    await api.deleteCard(cardId.value)
    router.back()
  }
}

onMounted(async () => {
  // Načti target_lang z dashboardu
  const { data: dashboard } = await api.getDashboard()
  for (const lang of dashboard) {
    for (const lesson of lang.lessons) {
      if (lesson.id === lessonId.value) {
        targetLang.value = lang.target_lang
        break
      }
    }
  }

  if (!isNew.value) {
    const { data } = await api.getCards(lessonId.value)
    const card = data.find(c => c.id === cardId.value)
    if (card) {
      front.value = card.fields.find(f => f.label === 'front')?.content || ''
      back.value = card.fields.find(f => f.label === 'back')?.content || ''
    }
  }
})
</script>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/CardListView.vue frontend/src/views/CardEditorView.vue frontend/src/router.js
git commit -m "feat: card list and card editor with auto-translate"
```

---

## Task 4: Import view

**Files:**
- Create: `frontend/src/views/ImportView.vue`
- Modify: `frontend/src/router.js`

- [ ] **Step 1: Přidej route**

```js
{ path: '/lessons/:lessonId/import', component: () => import('./views/ImportView.vue') },
```

- [ ] **Step 2: Vytvoř `ImportView.vue`**

```vue
<template>
  <AppLayout>
    <div class="p-6 max-w-lg mx-auto space-y-6">
      <h1 class="text-white font-bold text-lg">Import karet</h1>

      <!-- Drag & drop zone -->
      <div
        class="border-2 border-dashed border-gray-700 rounded-xl p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors"
        :class="{ 'border-indigo-500 bg-indigo-950/20': isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="handleDrop"
        @click="fileInput.click()"
      >
        <p class="text-gray-500 text-4xl mb-3">📁</p>
        <p class="text-gray-400 text-sm">Přetáhni CSV nebo JSON soubor</p>
        <p class="text-gray-600 text-xs mt-1">nebo klikni pro výběr</p>
        <input ref="fileInput" type="file" accept=".csv,.json" class="hidden" @change="handleFile" />
      </div>

      <!-- Formát nápověda -->
      <div class="bg-gray-900 rounded-lg p-4 text-xs text-gray-500 font-mono">
        <p class="text-gray-400 mb-1">CSV formát:</p>
        <p>front,back</p>
        <p>Hello,Ahoj</p>
      </div>

      <!-- Výsledek -->
      <div v-if="result" class="bg-gray-900 rounded-lg p-4 text-sm">
        <p class="text-green-400">✓ Importováno: {{ result.imported }}</p>
        <p v-if="result.skipped > 0" class="text-yellow-500">⚠ Přeskočeno (duplicity): {{ result.skipped }}</p>
      </div>

      <button @click="$router.back()" class="text-gray-500 text-sm">← Zpět</button>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const lessonId = route.params.lessonId
const isDragging = ref(false)
const result = ref(null)
const fileInput = ref(null)

async function importFile(file) {
  const { data } = await api.importCards(lessonId, file)
  result.value = data
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) importFile(file)
}

function handleFile(e) {
  const file = e.target.files[0]
  if (file) importFile(file)
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/ImportView.vue frontend/src/router.js
git commit -m "feat: CSV/JSON import view with drag and drop"
```

---

## Task 5: Statistiky

**Files:**
- Create: `frontend/src/views/StatsView.vue`
- Modify: `frontend/src/router.js`
- Modify: `backend/app/routers/` — přidej stats endpoint

- [ ] **Step 1: Přidej backend stats endpoint**

`GET /api/stats` — vrátí:
```json
{
  "streak_days": 7,
  "total_reviews_today": 23,
  "accuracy_7days": [0.8, 0.75, 0.9, 0.85, 0.7, 0.88, 0.92],
  "total_learned": 142,
  "total_cards": 247
}
```

Streak = počet po sobě jdoucích dní kdy uživatel hodnotil alespoň 1 kartu (z `CardProgress.last_reviewed`).

- [ ] **Step 2: Přidej endpoint do `api.js`**

```js
getStats: () => http.get('/stats'),
```

- [ ] **Step 3: Vytvoř `StatsView.vue`**

```vue
<template>
  <AppLayout>
    <div class="p-6 max-w-2xl mx-auto space-y-6">
      <h1 class="text-white font-bold text-lg">Statistiky</h1>

      <!-- Streak + celkové čísla -->
      <div class="grid grid-cols-3 gap-4">
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-indigo-400 text-3xl font-bold">{{ stats?.streak_days ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">streak dní 🔥</p>
        </div>
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-green-400 text-3xl font-bold">{{ stats?.total_learned ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">naučených karet</p>
        </div>
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-white text-3xl font-bold">{{ stats?.total_reviews_today ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">hodnocení dnes</p>
        </div>
      </div>

      <!-- Graf přesnosti 7 dní -->
      <div class="bg-gray-900 rounded-xl p-4">
        <p class="text-gray-400 text-xs uppercase tracking-wider mb-4">Přesnost za 7 dní</p>
        <div class="flex items-end gap-2 h-24">
          <div
            v-for="(val, i) in accuracy"
            :key="i"
            class="flex-1 bg-indigo-600 rounded-t-sm transition-all"
            :style="{ height: `${val * 100}%` }"
            :title="`${Math.round(val * 100)}%`"
          />
        </div>
        <div class="flex justify-between text-gray-600 text-xs mt-2">
          <span>před 6 dny</span>
          <span>dnes</span>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const stats = ref(null)
const accuracy = computed(() => stats.value?.accuracy_7days ?? Array(7).fill(0))

onMounted(async () => {
  const { data } = await api.getStats()
  stats.value = data
})
</script>
```

- [ ] **Step 4: Přidej route a link v sidebaru**

```js
{ path: '/stats', component: () => import('./views/StatsView.vue') },
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/StatsView.vue frontend/src/router.js backend/
git commit -m "feat: statistics view with streak and accuracy chart"
```

---

## Task 6: Navigace z sidebaru do lekcí

**Files:**
- Modify: `frontend/src/components/sidebar/LessonItem.vue`

- [ ] **Step 1: Přidej link na seznam karet** — kliknutí na název lekce (ne checkbox) otevře `/lessons/{id}/cards`

```vue
<router-link :to="`/lessons/${lesson.id}/cards`" class="flex-1 truncate text-xs" ...>
  {{ lesson.name }}
</router-link>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/sidebar/LessonItem.vue
git commit -m "feat: lesson name links to card list"
```

---

## Task 7: Finální testování + polish

- [ ] **Step 1: Projdi celý flow**
  1. Přidej jazyk "Angličtina 🇬🇧"
  2. Přidej lekci "Základní slovíčka"
  3. Importuj CSV s 10 slovíčky
  4. Vyber lekci → Začít → projdi celou session
  5. Reload stránky uprostřed session → ověř recovery dialog
  6. Přejmenuj lekci přes ⋯ menu
  7. Smaž jednu kartu
  8. Zkontroluj statistiky

- [ ] **Step 2: Ověř na mobilním viewportu** (DevTools → toggle device toolbar)
  - Hamburger menu funguje
  - Karta je fullscreen
  - Hodnoticí tlačítka jsou dostupná

- [ ] **Step 3: Docker compose build a test**

```bash
docker compose build
docker compose up
docker compose exec backend alembic upgrade head
# Otevři http://localhost
```

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete flashcards app v1"
```

---

## Hotovo — v1 kompletní

Na konci tohoto plánu:
- ✅ Kontextová menu (přejmenovat, reset progressu, smazat)
- ✅ Přidávání jazyků a lekcí přes sidebar
- ✅ Seznam karet lekce
- ✅ Editor karty s auto-překladem (debounce 1s)
- ✅ Import CSV/JSON s drag & drop
- ✅ Statistiky (streak, přesnost, grafy)
- ✅ Celá aplikace funguje v Dockeru
