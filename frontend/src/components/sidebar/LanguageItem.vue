<template>
  <div>
    <div class="flex items-center gap-2 px-2 py-2 rounded-lg cursor-pointer hover:bg-gray-800"
         @click="store.setExpanded(language.id, !store.isExpanded(language.id))">
      <span class="text-gray-500 text-xs w-3">{{ store.isExpanded(language.id) ? '▼' : '▶' }}</span>
      <span class="text-lg">{{ language.emoji }}</span>
      <span class="flex-1 text-sm font-semibold text-gray-200 truncate">{{ language.name }}</span>
      <span class="text-green-400 text-xs font-bold">{{ language.learned_cards }}</span>
      <span class="text-gray-600 text-xs">/{{ language.total_cards }}</span>
      <ContextMenu :show-settings="true" @settings="showSettings = true" @rename="showRename = true" @reset="handleReset" @delete="showConfirm = true" />
    </div>
    <div v-if="store.isExpanded(language.id)" class="pl-5 space-y-0.5 mt-0.5">
      <LessonItem v-for="lesson in language.lessons" :key="lesson.id" :lesson="lesson" :language-id="language.id" />
      <div v-if="showAddLesson" class="px-2 py-2 space-y-2 bg-gray-800 rounded-lg mt-1">
        <input v-model="newLessonName" placeholder="Název lekce" class="w-full bg-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" @keyup.enter="addLesson" autofocus />
        <div class="flex gap-2">
          <button @click="addLesson" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-3 py-1.5 rounded-lg flex-1">Přidat</button>
          <button @click="showAddLesson = false" class="text-gray-400 text-xs px-2 py-1.5 rounded-lg">Zrušit</button>
        </div>
      </div>
      <button v-else @click.stop="showAddLesson = true" class="w-full text-left text-xs text-gray-600 hover:text-gray-400 px-2 py-1.5 mt-0.5">
        + Přidat lekci
      </button>
    </div>

    <LanguageSettingsDialog v-if="showSettings" :initial-direction-mode="language.direction_mode" @confirm="handleSettings" @cancel="showSettings = false" />
    <EditLanguageDialog v-if="showRename" :initial-name="language.name" :initial-emoji="language.emoji" :initial-source-lang="language.source_lang" @confirm="handleRename" @cancel="showRename = false" />
    <ConfirmDialog
      v-if="showConfirm"
      title="Smazat jazyk"
      :message="`Opravdu smazat jazyk &quot;${language.name}&quot; a všechny jeho lekce a karty?`"
      @confirm="handleDelete"
      @cancel="showConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useLanguagesStore } from '../../stores/languages'
import { api } from '../../api'
import LessonItem from './LessonItem.vue'
import ContextMenu from './ContextMenu.vue'
import EditLanguageDialog from '../modals/EditLanguageDialog.vue'
import LanguageSettingsDialog from '../modals/LanguageSettingsDialog.vue'
import ConfirmDialog from '../modals/ConfirmDialog.vue'

const props = defineProps({ language: Object })
const store = useLanguagesStore()
const showRename = ref(false)
const showSettings = ref(false)
const showConfirm = ref(false)
const showAddLesson = ref(false)
const newLessonName = ref('')

async function handleRename({ name, emoji, source_lang }) {
  showRename.value = false
  await api.updateLanguage(props.language.id, { name, emoji, source_lang })
  await store.fetchDashboard()
}

async function handleSettings({ direction_mode }) {
  showSettings.value = false
  await api.updateLanguage(props.language.id, { direction_mode })
  await store.fetchDashboard()
}

async function handleReset() {
  await api.resetLanguageProgress(props.language.id)
  await store.fetchDashboard()
}

async function handleDelete() {
  showConfirm.value = false
  await store.deleteLanguage(props.language.id)
}

async function addLesson() {
  if (!newLessonName.value.trim()) return
  await api.createLesson({ language_id: props.language.id, name: newLessonName.value.trim() })
  newLessonName.value = ''
  showAddLesson.value = false
  await store.fetchDashboard()
}
</script>
