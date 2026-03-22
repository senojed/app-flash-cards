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
