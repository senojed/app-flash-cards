import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api'

export const useLanguagesStore = defineStore('languages', () => {
  const languages = ref([])
  const selectedLessonIds = ref(new Set())

  async function fetchDashboard() {
    const { data } = await api.getDashboard()
    languages.value = data
  }

  function toggleLesson(lessonId) {
    if (selectedLessonIds.value.has(lessonId)) {
      selectedLessonIds.value.delete(lessonId)
    } else {
      selectedLessonIds.value.add(lessonId)
    }
  }

  const selectedCount = computed(() => selectedLessonIds.value.size)

  async function deleteLanguage(id) {
    await api.deleteLanguage(id)
    await fetchDashboard()
  }

  async function deleteLesson(id) {
    await api.deleteLesson(id)
    selectedLessonIds.value.delete(id)
    await fetchDashboard()
  }

  return { languages, selectedLessonIds, selectedCount, fetchDashboard, toggleLesson, deleteLanguage, deleteLesson }
})
