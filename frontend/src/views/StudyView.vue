<template>
  <AppLayout>
    <!-- Main studijní area — přesně jako v návrhu -->
    <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; padding:32px; position:relative; margin:-24px; min-height:calc(100% + 48px)">
      <!-- Radial gradient pozadí (jako v návrhu .main::before) -->
      <div style="position:absolute; width:800px; height:500px; background:radial-gradient(ellipse,rgba(109,40,217,0.08) 0%,transparent 70%); top:50%; left:50%; transform:translate(-50%,-50%); pointer-events:none; z-index:0"></div>

      <!-- Session recovery dialog -->
      <div v-if="showRecovery" style="position:fixed; inset:0; background:rgba(0,0,0,0.7); display:flex; align-items:center; justify-content:center; z-index:50">
        <div style="background:#211d2f; border:1px solid #2d2840; border-radius:16px; padding:24px; text-align:center">
          <p style="color:white; font-weight:600; margin-bottom:16px">Máš rozdělanou session. Pokračovat?</p>
          <div style="display:flex; gap:12px; justify-content:center">
            <button @click="resumeSession" style="background:#7c3aed; color:white; padding:8px 16px; border-radius:8px; border:none; font-size:13px; font-weight:600; cursor:pointer">Pokračovat</button>
            <button @click="discardSession" style="background:#2a2540; color:white; padding:8px 16px; border-radius:8px; border:none; font-size:13px; cursor:pointer">Začít znovu</button>
          </div>
        </div>
      </div>

      <!-- Načítání -->
      <div v-if="loading" style="color:#52525b; font-size:13px; position:relative; z-index:1">Načítám karty...</div>

      <!-- Žádné karty dnes -->
      <div v-else-if="!loading && store.cards.length === 0" style="text-align:center; position:relative; z-index:1">
        <p style="font-size:40px; margin-bottom:16px">✅</p>
        <p style="color:white; font-weight:600; font-size:16px; margin-bottom:8px">Žádné karty ke studiu!</p>
        <p style="color:#71717a; font-size:13px; margin-bottom:20px">Všechny karty jsou naučeny nebo nejsou splatné.</p>
        <div style="display:flex; flex-direction:column; gap:12px; align-items:center">
          <button @click="studyAll"
            style="background:linear-gradient(135deg,#7c3aed,#6d28d9); color:white; padding:12px 24px; border-radius:11px; border:none; font-size:14px; font-weight:800; cursor:pointer; width:256px; box-shadow:0 4px 20px rgba(124,58,237,0.4); letter-spacing:0.5px; text-transform:uppercase">
            ▶ Procvičit vše
          </button>
          <button @click="$router.push('/')"
            style="background:#2a2540; color:#a1a1aa; padding:12px 24px; border-radius:11px; border:none; font-size:14px; cursor:pointer; width:256px">
            ← Dashboard
          </button>
        </div>
      </div>

      <template v-else-if="store.cards.length > 0">
        <!-- Progress row -->
        <div style="display:flex; align-items:center; justify-content:space-between; width:100%; max-width:500px; position:relative; z-index:1">
          <span style="font-size:12px; color:#52525b">Karta <strong style="color:#e2e8f0">{{ store.currentIndex }}</strong> / {{ store.cards.length }}</span>
          <UndoButton :can-undo="store.history.length > 0" @undo="store.undo()" />
        </div>

        <!-- Progress bar -->
        <div style="width:100%; max-width:500px; height:8px; background:#2d2840; border-radius:99px; overflow:hidden; position:relative; z-index:1">
          <div style="height:100%; border-radius:99px; background:linear-gradient(90deg,#7c3aed,#a78bfa,#7c3aed); background-size:200% 100%; animation:shimmer 2s infinite linear; box-shadow:0 0 12px rgba(167,139,250,0.5); transition:width 0.3s"
               :style="{ width: `${(store.currentIndex / Math.max(store.cards.length, 1)) * 100}%` }" />
        </div>

        <!-- Karta nebo finish -->
        <template v-if="!store.isFinished && store.currentCard">
          <StudyCard
            :card="store.currentCard"
            :revealed="store.revealed"
            :slide-class="slideClass"
            :source-lang="sourceLang"
            :target-lang="targetLang"
            @reveal="store.reveal()"
          />
          <RatingButtons v-if="store.revealed" @rate="handleRate" />
          <p v-else style="font-size:11px; color:#3f3f60; position:relative; z-index:1">Klikni na kartu pro odhalení</p>
        </template>

        <div v-else-if="store.isFinished" style="text-align:center; position:relative; z-index:1">
          <p style="font-size:40px; margin-bottom:16px">🎉</p>
          <p style="color:white; font-weight:600; font-size:16px; margin-bottom:20px">Session dokončena!</p>
          <div style="display:flex; flex-direction:column; gap:12px; align-items:center">
            <button @click="studyAll"
              style="background:linear-gradient(135deg,#7c3aed,#6d28d9); color:white; padding:12px 24px; border-radius:11px; border:none; font-size:14px; font-weight:800; cursor:pointer; width:256px; box-shadow:0 4px 20px rgba(124,58,237,0.4); letter-spacing:0.5px; text-transform:uppercase">
              ▶ Procvičit znovu
            </button>
            <button @click="$router.push('/')"
              style="background:#2a2540; color:#a1a1aa; padding:12px 24px; border-radius:11px; border:none; font-size:14px; cursor:pointer; width:256px">
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
const targetLang = ref('')
const slideClass = ref('')

watch(() => store.animationDirection, (dir) => {
  if (dir) slideClass.value = dir === 'left' ? 'slide-left' : 'slide-right'
})

onMounted(async () => {
  if (langStore.languages.length === 0) await langStore.fetchDashboard()

  const lessonParam = route.query.lessons
  if (lessonParam) {
    currentLessonIds.value = lessonParam.split(',')
    for (const lang of langStore.languages) {
      if (lang.lessons.some(l => currentLessonIds.value.includes(l.id))) {
        sourceLang.value = lang.source_lang || ''
        targetLang.value = lang.target_lang || ''
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
  if (!saved?.lessonIds) { router.push('/'); return }
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
  loading.value = true
  await store.startSessionForce(currentLessonIds.value)
  loading.value = false
}

async function handleRate(quality) {
  await store.rate(quality)
}

watch(() => route.query.t, async (t) => {
  if (!t || !route.query.lessons) return
  currentLessonIds.value = route.query.lessons.split(',')
  loading.value = true
  await store.startSession(currentLessonIds.value)
  loading.value = false
})
</script>
