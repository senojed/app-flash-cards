<template>
  <header class="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <button @click="$emit('menu')" class="text-gray-400 text-xl">☰</button>
      <router-link to="/" class="text-gray-400 text-lg">🏠</router-link>
      <button
        v-if="isStudying"
        @click="cancelStudy"
        class="w-8 h-8 rounded-full bg-red-700 hover:bg-red-600 flex items-center justify-center text-white font-bold text-sm"
      >✕</button>
    </div>
    <span class="text-indigo-400 font-bold text-sm">FlashCards</span>
    <span class="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-xs">👤</span>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useStudyStore } from '../../stores/study'

defineEmits(['menu'])

const route = useRoute()
const router = useRouter()
const studyStore = useStudyStore()

const isStudying = computed(() =>
  route.path === '/study' && studyStore.cards.length > 0 && !studyStore.isFinished
)

function cancelStudy() {
  studyStore.clearSession()
  router.push('/')
}
</script>
