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
      <div v-if="showAddLang" class="px-2 pb-2 space-y-1">
        <input v-model="newLangName" placeholder="Název jazyka" class="w-full bg-gray-800 rounded px-2 py-1 text-xs text-white" @keyup.enter="addLanguage" />
        <input v-model="newLangEmoji" placeholder="🏳️" class="w-16 bg-gray-800 rounded px-2 py-1 text-xs text-white" />
        <div class="flex gap-1">
          <button @click="addLanguage" class="bg-indigo-600 text-white text-xs px-2 py-1 rounded flex-1">Přidat</button>
          <button @click="showAddLang = false" class="text-gray-500 text-xs px-2 py-1">Zrušit</button>
        </div>
      </div>
      <button v-else @click="showAddLang = true" class="w-full text-left text-xs text-gray-600 hover:text-gray-400 px-2 py-1">
        + Přidat jazyk
      </button>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguagesStore } from '../../stores/languages'
import { api } from '../../api'
import LanguageItem from '../sidebar/LanguageItem.vue'

const store = useLanguagesStore()
const router = useRouter()
const showAddLang = ref(false)
const newLangName = ref('')
const newLangEmoji = ref('')

function startStudy() {
  router.push({ path: '/study', query: { lessons: [...store.selectedLessonIds].join(',') } })
}

async function addLanguage() {
  if (!newLangName.value.trim()) return
  await api.createLanguage({ name: newLangName.value.trim(), emoji: newLangEmoji.value.trim() || '🏳️' })
  newLangName.value = ''
  newLangEmoji.value = ''
  showAddLang.value = false
  await store.fetchDashboard()
}
</script>
