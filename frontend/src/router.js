import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from './views/DashboardView.vue'
import StudyView from './views/StudyView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardView },
    { path: '/study', component: StudyView },
    { path: '/lessons/:lessonId/cards', component: () => import('./views/CardListView.vue') },
    { path: '/lessons/:lessonId/cards/new', component: () => import('./views/CardEditorView.vue') },
    { path: '/cards/:cardId/edit', component: () => import('./views/CardEditorView.vue') },
    { path: '/lessons/:lessonId/import', component: () => import('./views/ImportView.vue') },
    { path: '/stats', component: () => import('./views/StatsView.vue') },
  ]
})
