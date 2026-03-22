import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export const api = {
  // Dashboard
  getDashboard: () => http.get('/languages/dashboard'),

  // Languages
  getLanguages: () => http.get('/languages'),
  createLanguage: (data) => http.post('/languages', data),
  updateLanguage: (id, data) => http.patch(`/languages/${id}`, data),
  deleteLanguage: (id) => http.delete(`/languages/${id}`),
  resetLanguageProgress: (id) => http.delete(`/languages/${id}/progress`),

  // Lessons
  getLessons: (languageId) => http.get('/lessons', { params: { language_id: languageId } }),
  createLesson: (data) => http.post('/lessons', data),
  updateLesson: (id, data) => http.patch(`/lessons/${id}`, data),
  deleteLesson: (id) => http.delete(`/lessons/${id}`),
  resetLessonProgress: (id) => http.delete(`/lessons/${id}/progress`),

  // Cards
  getCards: (lessonId) => http.get('/cards', { params: { lesson_id: lessonId } }),
  createCard: (data) => http.post('/cards', data),
  updateCard: (id, data) => http.patch(`/cards/${id}`, data),
  deleteCard: (id) => http.delete(`/cards/${id}`),
  uploadMedia: (cardId, label, file) => {
    const form = new FormData()
    form.append('file', file)
    return http.post(`/cards/${cardId}/media/${label}`, form)
  },

  // Study
  getStudyCards: (lessonIds) => http.post('/study/cards', { lesson_ids: lessonIds }),
  rateCard: (data) => http.post('/study/rate', data),
  undoRating: (previousState) => http.post('/study/undo', previousState),

  // Import
  importCards: (lessonId, file) => {
    const form = new FormData()
    form.append('lesson_id', lessonId)
    form.append('file', file)
    return http.post('/import', form)
  },

  // Translate
  translate: (text, targetLang) => http.post('/translate', { text, target_lang: targetLang }),

  // Stats
  getStats: () => http.get('/stats'),
}
