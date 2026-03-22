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
          @reveal="store.reveal()"
        />
        <RatingButtons v-if="store.revealed" @rate="handleRate" />
        <p v-else class="text-gray-600 text-xs">Klikni na kartu pro odhalení</p>
      </template>

      <div v-else-if="store.isFinished" class="text-center space-y-4">
        <p class="text-4xl">🎉</p>
        <p class="text-white font-semibold">Session dokončena!</p>
        <button @click="$router.push('/')" class="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm">
          Zpět na Dashboard
        </button>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStudyStore } from '../stores/study'
import AppLayout from '../components/layout/AppLayout.vue'
import StudyCard from '../components/study/StudyCard.vue'
import RatingButtons from '../components/study/RatingButtons.vue'
import UndoButton from '../components/study/UndoButton.vue'

const route = useRoute()
const router = useRouter()
const store = useStudyStore()
const showRecovery = ref(false)
const slideClass = computed(() =>
  store.animationDirection === 'left' ? 'slide-left' : 'slide-right'
)

onMounted(async () => {
  const lessonParam = route.query.lessons

  if (lessonParam) {
    // Vždy začni novou session pokud jsou předány lekce
    store.clearSession()
    const lessonIds = lessonParam.split(',')
    await store.startSession(lessonIds)
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
  await store.startSession(saved.lessonIds)
  store.currentIndex = saved.currentIndex
}

function discardSession() {
  store.clearSession()
  showRecovery.value = false
  router.push('/')
}

async function handleRate(quality) {
  await store.rate(quality)
}
</script>
