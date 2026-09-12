<template>
  <div style="display:flex; align-items:center; gap:8px; padding:7px 10px; border-radius:8px; cursor:pointer; font-size:12px; margin-bottom:2px; transition:all 0.12s"
       :style="isSelected ? 'background:#2a1f45; color:#c4b5fd' : 'color:#6b7280'"
       @mouseover="!isSelected && ($event.currentTarget.style.background='#2a2540') && ($event.currentTarget.style.color='#a1a1aa')"
       @mouseout="!isSelected && ($event.currentTarget.style.background='') && ($event.currentTarget.style.color='#6b7280')">
    <!-- Checkbox -->
    <div style="width:16px; height:16px; border-radius:4px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; cursor:pointer"
         :style="isSelected ? 'background:#7c3aed; color:white' : 'border:1.5px solid #3f3f60'"
         @click.stop="store.toggleLesson(lesson.id)">
      <span v-if="isSelected">✓</span>
    </div>
    <router-link :to="`/lessons/${lesson.id}/cards`"
      style="flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-decoration:none; color:inherit"
      @click.stop>
      {{ lesson.name }}
    </router-link>
    <span style="font-size:10px; font-weight:700; color:#a78bfa; flex-shrink:0">{{ lesson.learned_cards }}</span>
    <span style="font-size:10px; color:#3f3f60; flex-shrink:0">/{{ lesson.total_cards }}</span>
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
