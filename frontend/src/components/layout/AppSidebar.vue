<template>
  <aside class="w-64 bg-gray-900 flex flex-col border border-gray-800 rounded-2xl shrink-0 overflow-hidden">
    <!-- Header -->
    <div class="px-4 py-4 border-b border-gray-800 flex items-center justify-between">
      <span class="text-indigo-400 font-bold text-base">📚 FlashCards <span class="text-gray-500 text-xs font-normal">v0.9</span></span>
    </div>

    <!-- Desktop: Language tree -->
    <div v-if="!isMobile" class="flex-1 overflow-y-auto p-3 space-y-1">
      <LanguageItem
        v-for="lang in store.languages"
        :key="lang.id"
        :language="lang"
      />

      <!-- Přidat jazyk -->
      <div v-if="showAddLang" class="mt-2 space-y-2 bg-gray-800 rounded-lg p-3">
        <input
          v-model="newLangName"
          placeholder="Název jazyka (např. Angličtina)"
          class="w-full bg-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          @keyup.enter="addLanguage"
          autofocus
        />
        <div class="flex gap-2 items-center">
          <input
            v-model="newLangEmoji"
            placeholder="🏳️ emoji"
            class="w-24 bg-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <span class="text-gray-500 text-xs flex-1">vlajka/emoji</span>
        </div>
        <div class="flex gap-2">
          <button @click="addLanguage" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm px-3 py-1.5 rounded-lg flex-1 font-medium">Přidat</button>
          <button @click="showAddLang = false" class="text-gray-400 hover:text-gray-200 text-sm px-3 py-1.5 rounded-lg">Zrušit</button>
        </div>
      </div>
      <button v-else @click="showAddLang = true" class="w-full text-left text-sm text-gray-500 hover:text-gray-300 px-2 py-2 mt-1">
        + Přidat jazyk
      </button>
    </div>

    <!-- Mobil: prázdný flex-1 -->
    <div v-else class="flex-1" />

    <!-- Start / Zrušit tlačítko (jen desktop) -->
    <div v-if="!isMobile" class="p-3 border-t border-gray-800">
      <button
        v-if="isStudying"
        @click="cancelStudy"
        class="w-full bg-red-800 hover:bg-red-700 text-white text-sm font-semibold py-2.5 rounded-lg"
      >
        ✕ Zrušit lekci
      </button>
      <button
        v-else-if="store.selectedCount > 0"
        @click="startStudy"
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold py-2.5 rounded-lg"
      >
        ▶ Začít vybrané ({{ store.selectedCount }})
      </button>
    </div>

    <!-- Nav -->
    <div class="p-3 border-t border-gray-800 space-y-1">
      <router-link to="/stats" class="flex items-center gap-2 px-3 py-2 text-sm text-gray-400 hover:text-white rounded-lg hover:bg-gray-800">
        📊 Statistiky
      </router-link>
      <button disabled class="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 cursor-not-allowed rounded-lg w-full text-left">
        ⚙️ Nastavení
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLanguagesStore } from '../../stores/languages'
import { useStudyStore } from '../../stores/study'
import { api } from '../../api'
import LanguageItem from '../sidebar/LanguageItem.vue'

const store = useLanguagesStore()
const studyStore = useStudyStore()
const router = useRouter()
const route = useRoute()
const showAddLang = ref(false)
const newLangName = ref('')
const newLangEmoji = ref('')
const isMobile = ref(false)

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => { checkMobile(); window.addEventListener('resize', checkMobile) })
onUnmounted(() => window.removeEventListener('resize', checkMobile))

const isStudying = computed(() =>
  route.path === '/study' && studyStore.cards.length > 0 && !studyStore.isFinished
)


function startStudy() {
  const ids = store.selectedCount > 0
    ? [...store.selectedLessonIds].join(',')
    : studyStore.currentLessonIds.join(',')
  router.push({ path: '/study', query: { lessons: ids, t: Date.now() } })
}

function cancelStudy() {
  studyStore.clearSession()
  router.push('/')
}

async function addLanguage() {
  if (!newLangName.value.trim()) return
  await api.createLanguage({ name: newLangName.value.trim(), emoji: newLangEmoji.value.trim() || '🌐' })
  newLangName.value = ''
  newLangEmoji.value = ''
  showAddLang.value = false
  await store.fetchDashboard()
}
</script>
