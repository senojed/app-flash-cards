<template>
  <AppLayout>
    <!-- Desktop: placeholder -->
    <div v-if="!isMobile" class="flex items-center justify-center h-full text-gray-600 text-sm">
      <div class="text-center">
        <p class="text-4xl mb-4">📚</p>
        <p>Vyber lekce v postranním panelu a klikni Začít.</p>
      </div>
    </div>

    <!-- Mobil: seznam jazyků a lekcí -->
    <div v-else class="space-y-4">
      <div v-for="lang in store.languages" :key="lang.id" class="space-y-2">
        <div class="flex items-center gap-2 px-1">
          <span class="flex-1 font-bold text-gray-200">{{ lang.emoji }} {{ lang.name }}</span>
          <span class="text-green-400 text-xs">{{ lang.learned_cards }}</span>
          <span class="text-gray-600 text-xs">/{{ lang.total_cards }}</span>
          <button @click.stop="openSettings(lang)" class="text-gray-500 hover:text-gray-300 px-1">⚙️</button>
        </div>
        <div class="space-y-1">
          <div
            v-for="lesson in lang.lessons"
            :key="lesson.id"
            class="flex items-center gap-3 bg-gray-800 rounded-xl px-4 py-3"
          >
            <input
              type="checkbox"
              :checked="store.selectedLessonIds.has(lesson.id)"
              @change="store.toggleLesson(lesson.id)"
              class="w-5 h-5 accent-indigo-500"
            />
            <span class="flex-1 text-gray-200">{{ lesson.name }}</span>
            <span class="text-green-400 text-xs">{{ lesson.learned_cards }}</span>
            <span class="text-gray-600 text-xs">/{{ lesson.total_cards }}</span>
            <router-link :to="`/lessons/${lesson.id}/cards`" class="text-gray-500 text-xs hover:text-gray-300">→</router-link>
          </div>
        </div>
      </div>

      <!-- Start tlačítko -->
      <div v-if="store.selectedCount > 0" class="sticky bottom-0 pt-3">
        <button
          @click="startStudy"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl"
        >
          ▶ Začít vybrané ({{ store.selectedCount }})
        </button>
      </div>
    </div>

    <LanguageSettingsDialog v-if="settingsLang" :initial-direction-mode="settingsLang.direction_mode" @confirm="handleSettings" @cancel="settingsLang = null" />
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguagesStore } from '../stores/languages'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'
import LanguageSettingsDialog from '../components/modals/LanguageSettingsDialog.vue'

const store = useLanguagesStore()
const router = useRouter()
const isMobile = ref(false)
const settingsLang = ref(null)

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  store.fetchDashboard()
})
onUnmounted(() => window.removeEventListener('resize', checkMobile))

function startStudy() {
  router.push({ path: '/study', query: { lessons: [...store.selectedLessonIds].join(',') } })
}

function openSettings(lang) { settingsLang.value = lang }

async function handleSettings({ direction_mode }) {
  await api.updateLanguage(settingsLang.value.id, { direction_mode })
  settingsLang.value = null
  await store.fetchDashboard()
}
</script>
