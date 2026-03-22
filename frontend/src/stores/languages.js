import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api'

export const useLanguagesStore = defineStore('languages', () => {
  const languages = ref([])
  const selectedLessonIds = ref(new Set())
  const expandedLanguages = ref(new Set())

  async function fetchDashboard() {
    const { data } = await api.getDashboard()
    languages.value = data
      .sort((a, b) => a.name.localeCompare(b.name, 'cs'))
      .map(lang => ({
        ...lang,
        lessons: [...lang.lessons].sort((a, b) => a.name.localeCompare(b.name, 'cs'))
      }))
    // Nové jazyky jsou výchozně rozbalené
    for (const lang of languages.value) {
      if (!expandedLanguages.value.has(lang.id)) {
        expandedLanguages.value.add(lang.id)
      }
    }
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

  function setExpanded(langId, val) {
    if (val) expandedLanguages.value.add(langId)
    else expandedLanguages.value.delete(langId)
  }

  function isExpanded(langId) {
    return expandedLanguages.value.has(langId)
  }

  return { languages, selectedLessonIds, selectedCount, expandedLanguages, fetchDashboard, toggleLesson, deleteLanguage, deleteLesson, setExpanded, isExpanded }
})
