<template>
  <AppLayout>
    <div class="p-6 max-w-2xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-white font-bold text-lg">{{ lessonName }}</h1>
        <div class="flex gap-2">
          <router-link :to="`/lessons/${lessonId}/import`" class="bg-gray-700 text-white text-xs px-3 py-2 rounded-lg">📥 Import</router-link>
          <router-link :to="`/lessons/${lessonId}/cards/new`" class="bg-indigo-600 text-white text-xs px-3 py-2 rounded-lg">+ Přidat kartu</router-link>
        </div>
      </div>

      <div class="space-y-2">
        <router-link
          v-for="card in cards"
          :key="card.id"
          :to="`/cards/${card.id}/edit`"
          class="flex items-center gap-4 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-lg px-4 py-3"
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const lessonId = route.params.lessonId
const cards = ref([])
const lessonName = ref('')

onMounted(async () => {
  const { data } = await api.getCards(lessonId)
  cards.value = data

  const { data: dashboard } = await api.getDashboard()
  for (const lang of dashboard) {
    const lesson = lang.lessons.find(l => l.id === lessonId)
    if (lesson) { lessonName.value = lesson.name; break }
  }
})

function getField(card, label) {
  return card.fields.find(f => f.label === label)?.content ?? ''
}
</script>
