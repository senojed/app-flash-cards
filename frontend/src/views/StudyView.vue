<template>
  <AppLayout>
    <div class="flex flex-col items-center justify-center h-full gap-6 p-4">

      <!-- Session recovery dialog -->
      <div v-if="showRecovery" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="bg-gray-900 rounded-xl p-6 text-center space-y-4">
          <p class="text-white font-semibold">Máš rozdělanou session. Pokračovat?</p>
          <div class="flex gap-3 justify-center">
            <button @click="resumeSession" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Pokračovat</button>
            <button @click="discardSession" class="bg-gray-700 text-white px-4 py-2 rounded-lg text-sm">Začít znovu</button>
          </div>
        </div>
      </div>

      <!-- Načítání -->
      <div v-if="loading" class="text-gray-500 text-sm">Načítám karty...</div>

      <!-- Žádné karty dnes -->
      <div v-else-if="!loading && store.cards.length === 0" class="text-center space-y-4">
        <p class="text-4xl">✅</p>
        <p class="text-white font-semibold">Žádné karty ke studiu!</p>
        <p class="text-gray-400 text-sm">Všechny karty jsou naučeny nebo nejsou splatné.</p>
        <div class="flex flex-col gap-3 items-center">
          <button @click="studyAll" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl font-semibold w-64">
            ▶ Procvičit vše
          </button>
          <button @click="$router.push('/')" class="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-xl font-semibold w-64">
            ← Dashboard
          </button>
        </div>
      </div>

      <template v-else-if="store.cards.length > 0">
        <!-- Progress + Undo -->
        <div class="flex items-center justify-between w-80">
          <span class="text-gray-500 text-xs">{{ store.currentIndex }} / {{ store.cards.length }}</span>
          <UndoButton :can-undo="store.history.length > 0" @undo="store.undo()" />
        </div>

        <!-- Progress bar -->
        <div class="w-80 bg-gray-800 rounded-full h-1">
          <div class="bg-indigo-500 h-1 rounded-full transition-all"
               :style="{ width: `${(store.currentIndex / Math.max(store.cards.length, 1)) * 100}%` }" />
        </div>

        <!-- Karta nebo finish -->
        <template v-if="!store.isFinished && store.currentCard">
          <StudyCard
            :card="store.currentCard"
            :revealed="store.revealed"
            :slide-class="slideClass"
            :source-lang="sourceLang"
            @reveal="store.reveal()"
          />
          <RatingButtons v-if="store.revealed" @rate="handleRate" />
          <p v-else class="text-gray-600 text-xs">Klikni na kartu pro odhalení</p>
        </template>

        <div v-else-if="store.isFinished" class="text-center space-y-4">
          <p class="text-4xl">🎉</p>
          <p class="text-white font-semibold">Session dokončena!</p>
          <div class="flex flex-col gap-3 items-center">
            <button @click="studyAll" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl font-semibold w-64">
              ▶ Procvičit znovu
            </button>
            <button @click="$router.push('/')" class="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-xl font-semibold w-64">
              ← Dashboard
            </button>
          </div>
        </div>
      </template>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStudyStore } from '../stores/study'
import { useLanguagesStore } from '../stores/languages'
import AppLayout from '../components/layout/AppLayout.vue'
import StudyCard from '../components/study/StudyCard.vue'
import RatingButtons from '../components/study/RatingButtons.vue'
import UndoButton from '../components/study/UndoButton.vue'

const route = useRoute()
const router = useRouter()
const store = useStudyStore()
const langStore = useLanguagesStore()
const showRecovery = ref(false)
const loading = ref(false)
const currentLessonIds = ref([])
const sourceLang = ref('')

const slideClass = ref('')

watch(() => store.animationDirection, (dir) => {
  if (dir) slideClass.value = dir === 'left' ? 'slide-left' : 'slide-right'
})

onMounted(async () => {
  // Vždy načti dashboard (oprava prázdného sidebaru po reloadu)
  if (langStore.languages.length === 0) {
    langStore.fetchDashboard()
  }

  const lessonParam = route.query.lessons

  if (lessonParam) {
    currentLessonIds.value = lessonParam.split(',')
    // Zjisti source_lang z prvního jazyka který obsahuje tyto lekce
    for (const lang of langStore.languages) {
      if (lang.lessons.some(l => currentLessonIds.value.includes(l.id))) {
        sourceLang.value = lang.source_lang || ''
        break
      }
    }
    loading.value = true
    await store.startSession(currentLessonIds.value)
    loading.value = false
    return
  }

  const saved = store.loadSavedSession()
  if (saved) {
    showRecovery.value = true
  } else {
    router.push('/')
  }
})

async function resumeSession() {
  showRecovery.value = false
  const saved = store.loadSavedSession()
  currentLessonIds.value = saved.lessonIds
  await store.startSession(saved.lessonIds)
  store.currentIndex = saved.currentIndex
}

function discardSession() {
  store.clearSession()
  showRecovery.value = false
  router.push('/')
}

async function studyAll() {
  // Procvičit vše — pošleme speciální flag nebo dočasně změníme due_date logiku
  // Jednodušší: reset progressu a začni znovu
  loading.value = true
  await store.startSessionForce(currentLessonIds.value)
  loading.value = false
}

async function handleRate(quality) {
  await store.rate(quality)
}
</script>
