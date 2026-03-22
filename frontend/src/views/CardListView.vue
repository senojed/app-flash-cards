<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/')" class="text-gray-400 hover:text-white text-sm">← Zpět</button>
          <h1 class="text-white font-bold text-lg">{{ languageEmoji }} {{ lessonName }}</h1>
        </div>
        <div class="flex gap-2">
          <router-link :to="`/lessons/${lessonId}/import`" class="bg-gray-700 text-white text-xs px-3 py-2 rounded-lg">📥 Import</router-link>
          <router-link :to="`/lessons/${lessonId}/cards/new`" class="bg-indigo-600 text-white text-xs px-3 py-2 rounded-lg">+ Přidat kartu</router-link>
        </div>
      </div>

      <div class="space-y-2">
        <router-link
          v-for="card in cards"
          :key="card.id"
          :to="`/cards/${card.id}/edit?lessonId=${lessonId}`"
          class="flex items-center gap-4 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-lg px-6 py-3"
        >
          <span class="text-white text-sm flex-1">{{ getField(card, 'front') }}</span>
          <span class="text-gray-500 text-sm flex-1">{{ getField(card, 'back') }}</span>
          <span class="text-xs" v-if="getField(card, 'front_image')">🖼</span>
          <span class="text-xs" v-if="getField(card, 'front_audio')">🔊</span>
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useLanguagesStore } from '../stores/languages'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const langStore = useLanguagesStore()
const lessonId = computed(() => route.params.lessonId)
const cards = ref([])
const lessonName = ref('')
const languageEmoji = ref('')

async function loadLesson(lessonId) {
  const { data } = await api.getCards(lessonId)
  cards.value = data
  for (const lang of langStore.languages) {
    const lesson = lang.lessons.find(l => l.id === lessonId)
    if (lesson) { lessonName.value = lesson.name; languageEmoji.value = lang.emoji; break }
  }
}

watch(() => route.params.lessonId, (id) => { if (id) loadLesson(id) }, { immediate: true })

function getField(card, label) {
  return card.fields.find(f => f.label === label)?.content ?? ''
}
</script>
