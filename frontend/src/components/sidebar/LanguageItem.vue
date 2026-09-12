<template>
  <div>
    <!-- Language card -->
    <div style="background:#2a2540; border-radius:10px; padding:10px 12px; margin-bottom:8px; cursor:pointer; transition:all 0.15s"
         @mouseover="$event.currentTarget.style.background='#302b4a'"
         @mouseout="$event.currentTarget.style.background='#2a2540'"
         @click="store.setExpanded(language.id, !store.isExpanded(language.id))">
      <!-- Header řádek -->
      <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px">
        <span style="font-size:10px; color:#52525b; width:12px">{{ store.isExpanded(language.id) ? '▼' : '▶' }}</span>
        <span style="font-size:14px">{{ language.emoji }}</span>
        <span style="flex:1; font-size:13px; font-weight:700; color:#e2e8f0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis">{{ language.name }}</span>
        <ContextMenu :show-settings="true" @settings="showSettings = true" @rename="showRename = true" @reset="handleReset" @delete="showConfirm = true" />
      </div>
      <!-- Progress bar -->
      <div style="height:4px; background:#1a1625; border-radius:99px; overflow:hidden">
        <div style="height:100%; border-radius:99px; background:linear-gradient(90deg,#7c3aed,#a78bfa); transition:width 0.3s"
             :style="{ width: progressPct + '%' }"></div>
      </div>
      <!-- Stats -->
      <div style="display:flex; justify-content:space-between; margin-top:5px">
        <span style="font-size:10px; color:#6b7280"><strong style="color:#a78bfa">{{ language.learned_cards }}</strong> naučeno</span>
        <span style="font-size:10px; color:#6b7280">{{ language.total_cards > 0 ? progressPct + '%' : '—' }}</span>
      </div>
    </div>

    <!-- Lekce -->
    <div v-if="store.isExpanded(language.id)" style="padding-left:4px; margin-bottom:4px">
      <LessonItem v-for="lesson in language.lessons" :key="lesson.id" :lesson="lesson" :language-id="language.id" />
      <div v-if="showAddLesson" style="padding:10px; background:#2a2540; border-radius:8px; margin-top:4px">
        <input v-model="newLessonName" placeholder="Název lekce"
               style="width:100%; background:#1a1625; border:1px solid #2d2840; border-radius:7px; padding:6px 10px; font-size:12px; color:white; outline:none; margin-bottom:6px"
               @keyup.enter="addLesson" autofocus />
        <div style="display:flex; gap:6px">
          <button @click="addLesson" style="background:#7c3aed; color:white; font-size:12px; font-weight:700; padding:6px 10px; border-radius:7px; border:none; flex:1; cursor:pointer">Přidat</button>
          <button @click="showAddLesson = false" style="font-size:12px; color:#71717a; padding:6px 8px; border-radius:7px; border:none; background:transparent; cursor:pointer">Zrušit</button>
        </div>
      </div>
      <button v-else @click.stop="showAddLesson = true"
        style="width:100%; text-align:left; font-size:11px; color:#52525b; padding:6px 10px; margin-top:2px; border-radius:8px; border:none; background:transparent; cursor:pointer"
        @mouseover="$event.target.style.color='#a78bfa'"
        @mouseout="$event.target.style.color='#52525b'">
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
import { ref, computed } from 'vue'
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

const progressPct = computed(() => {
  if (!props.language.total_cards) return 0
  return Math.round((props.language.learned_cards / props.language.total_cards) * 100)
})

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
