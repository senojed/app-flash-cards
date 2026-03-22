import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api'

const SESSION_KEY = 'flashcards_session'

export const useStudyStore = defineStore('study', () => {
  const cards = ref([])
  const currentIndex = ref(0)
  const history = ref([])  // [{card, quality, previousState}] — max 5
  const revealed = ref(false)
  const animationDirection = ref(null)  // 'left' | 'right' | null
  const currentLessonIds = ref([])

  const currentCard = computed(() => cards.value[currentIndex.value] ?? null)
  const isFinished = computed(() => currentIndex.value >= cards.value.length)

  async function startSession(lessonIds) {
    cards.value = []
    currentIndex.value = 0
    history.value = []
    revealed.value = false
    animationDirection.value = null
    currentLessonIds.value = lessonIds
    const { data } = await api.getStudyCards(lessonIds)
    cards.value = data
    saveSession(lessonIds)
  }

  async function startSessionForce(lessonIds) {
    cards.value = []
    currentIndex.value = 0
    history.value = []
    revealed.value = false
    animationDirection.value = null
    currentLessonIds.value = lessonIds
    const { data } = await api.getStudyCards(lessonIds, true)
    cards.value = data
    saveSession(lessonIds)
  }

  function saveSession(lessonIds) {
    localStorage.setItem(SESSION_KEY, JSON.stringify({
      lessonIds,
      cardIds: cards.value.map(c => c.card_id),
      currentIndex: currentIndex.value,
    }))
  }

  function loadSavedSession() {
    const raw = localStorage.getItem(SESSION_KEY)
    return raw ? JSON.parse(raw) : null
  }

  function clearSession() {
    localStorage.removeItem(SESSION_KEY)
  }

  function reveal() {
    revealed.value = true
  }

  async function rate(quality) {
    const card = currentCard.value
    if (!card) return

    animationDirection.value = quality <= 3 ? 'left' : 'right'

    const { data } = await api.rateCard({
      card_id: card.card_id,
      direction: card.direction,
      quality,
    })

    history.value = [
      { card, quality, previousState: data.previous_state },
      ...history.value,
    ].slice(0, 5)

    setTimeout(() => {
      currentIndex.value++
      revealed.value = false
      animationDirection.value = null
      saveSession(currentLessonIds.value)
    }, 300)
  }

  async function undo() {
    if (history.value.length === 0) return
    const last = history.value.shift()
    await api.undoRating(last.previousState)
    currentIndex.value--
    revealed.value = false
  }

  return {
    cards, currentIndex, history, revealed, animationDirection, currentLessonIds,
    currentCard, isFinished,
    startSession, startSessionForce, loadSavedSession, clearSession, reveal, rate, undo,
  }
})
