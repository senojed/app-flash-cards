<template>
  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm cursor-pointer hover:bg-gray-800"
       :class="isSelected ? 'bg-indigo-950' : ''">
    <input type="checkbox" :checked="isSelected" @change="store.toggleLesson(lesson.id)"
           class="accent-indigo-500 w-3.5 h-3.5 shrink-0" />
    <router-link :to="`/lessons/${lesson.id}/cards`" class="flex-1 truncate" :class="isSelected ? 'text-indigo-200' : 'text-gray-400'" @click.stop>
      {{ lesson.name }}
    </router-link>
    <span class="text-green-400 text-xs font-bold shrink-0">{{ lesson.learned_cards }}</span>
    <span class="text-gray-600 text-xs shrink-0">/{{ lesson.total_cards }}</span>
    <ContextMenu @rename="showRename = true" @reset="handleReset" @delete="showConfirm = true" />

    <RenameDialog v-if="showRename" :initial-value="lesson.name" @confirm="handleRename" @cancel="showRename = false" />
    <ConfirmDialog
      v-if="showConfirm"
      title="Smazat lekci"
      :message="`Opravdu smazat lekci &quot;${lesson.name}&quot; a všechny její karty?`"
      @confirm="handleDelete"
      @cancel="showConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useLanguagesStore } from '../../stores/languages'
import { api } from '../../api'
import ContextMenu from './ContextMenu.vue'
import RenameDialog from '../modals/RenameDialog.vue'
import ConfirmDialog from '../modals/ConfirmDialog.vue'

const props = defineProps({ lesson: Object, languageId: String })
const store = useLanguagesStore()
const isSelected = computed(() => store.selectedLessonIds.has(props.lesson.id))
const showRename = ref(false)
const showConfirm = ref(false)

async function handleRename(name) {
  showRename.value = false
  await api.updateLesson(props.lesson.id, { name })
  await store.fetchDashboard()
}

async function handleReset() {
  await api.resetLessonProgress(props.lesson.id)
  await store.fetchDashboard()
}

async function handleDelete() {
  showConfirm.value = false
  await store.deleteLesson(props.lesson.id)
}
</script>
