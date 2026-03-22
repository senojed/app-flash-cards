<template>
  <div>
    <div class="flex items-center gap-1 px-2 py-1 rounded cursor-pointer hover:bg-gray-800"
         @click="expanded = !expanded">
      <span class="text-gray-500 text-xs">{{ expanded ? '▼' : '▶' }}</span>
      <span class="text-sm">{{ language.emoji }}</span>
      <span class="flex-1 text-xs font-semibold text-gray-200 truncate">{{ language.name }}</span>
      <span class="text-green-400 text-xs font-bold">{{ language.learned_cards }}</span>
      <span class="text-gray-600 text-xs">/{{ language.total_cards }}</span>
      <ContextMenu @rename="showRename = true" @reset="handleReset" @delete="showConfirm = true" />
    </div>
    <div v-if="expanded" class="pl-4 space-y-0.5">
      <LessonItem v-for="lesson in language.lessons" :key="lesson.id" :lesson="lesson" :language-id="language.id" />
      <div v-if="showAddLesson" class="px-2 pb-1 space-y-1">
        <input v-model="newLessonName" placeholder="Název lekce" class="w-full bg-gray-800 rounded px-2 py-1 text-xs text-white" @keyup.enter="addLesson" />
        <div class="flex gap-1">
          <button @click="addLesson" class="bg-indigo-600 text-white text-xs px-2 py-1 rounded flex-1">Přidat</button>
          <button @click="showAddLesson = false" class="text-gray-500 text-xs px-2 py-1">Zrušit</button>
        </div>
      </div>
      <button v-else @click.stop="showAddLesson = true" class="w-full text-left text-xs text-gray-600 hover:text-gray-400 px-2 py-1">
        + Přidat lekci
      </button>
    </div>

    <RenameDialog v-if="showRename" :initial-value="language.name" @confirm="handleRename" @cancel="showRename = false" />
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
import RenameDialog from '../modals/RenameDialog.vue'
import ConfirmDialog from '../modals/ConfirmDialog.vue'

const props = defineProps({ language: Object })
const store = useLanguagesStore()
const expanded = ref(true)
const showRename = ref(false)
const showConfirm = ref(false)
const showAddLesson = ref(false)
const newLessonName = ref('')

async function handleRename(name) {
  showRename.value = false
  await api.updateLanguage(props.language.id, { name })
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
