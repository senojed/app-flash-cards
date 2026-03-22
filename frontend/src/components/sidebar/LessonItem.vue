<template>
  <div class="flex items-center gap-1 px-2 py-1 rounded text-xs cursor-pointer hover:bg-gray-800"
       :class="isSelected ? 'bg-indigo-950' : ''">
    <input type="checkbox" :checked="isSelected" @change="store.toggleLesson(lesson.id)"
           class="accent-indigo-500 w-3 h-3" />
    <span class="flex-1 truncate" :class="isSelected ? 'text-indigo-200' : 'text-gray-400'">
      {{ lesson.name }}
    </span>
    <span class="text-green-400 font-bold">{{ lesson.learned_cards }}</span>
    <span class="text-gray-600">/{{ lesson.total_cards }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguagesStore } from '../../stores/languages'

const props = defineProps({ lesson: Object })
const store = useLanguagesStore()
const isSelected = computed(() => store.selectedLessonIds.has(props.lesson.id))
</script>
