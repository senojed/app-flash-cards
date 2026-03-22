<template>
  <div>
    <div class="flex items-center gap-1 px-2 py-1 rounded cursor-pointer hover:bg-gray-800"
         @click="expanded = !expanded">
      <span class="text-gray-500 text-xs">{{ expanded ? '▼' : '▶' }}</span>
      <span class="text-sm">{{ language.emoji }}</span>
      <span class="flex-1 text-xs font-semibold text-gray-200 truncate">{{ language.name }}</span>
      <span class="text-green-400 text-xs font-bold">{{ language.learned_cards }}</span>
      <span class="text-gray-600 text-xs">/{{ language.total_cards }}</span>
    </div>
    <div v-if="expanded" class="pl-4 space-y-0.5">
      <LessonItem v-for="lesson in language.lessons" :key="lesson.id" :lesson="lesson" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LessonItem from './LessonItem.vue'

defineProps({ language: Object })
const expanded = ref(true)
</script>
