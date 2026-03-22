<template>
  <div class="relative">
    <button @click.stop="open = !open" class="text-gray-600 hover:text-gray-300 px-1">⋯</button>
    <div v-if="open" class="absolute right-0 top-5 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-30 w-36 py-1 text-xs">
      <button @click="emit('rename'); open = false" class="w-full text-left px-3 py-2 hover:bg-gray-700 text-gray-300">✏️ Přejmenovat</button>
      <button v-if="showReset" @click="emit('reset'); open = false" class="w-full text-left px-3 py-2 hover:bg-gray-700 text-gray-300">🔄 Reset progressu</button>
      <button @click="emit('delete'); open = false" class="w-full text-left px-3 py-2 hover:bg-red-900 text-red-400">🗑 Smazat</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ showReset: { type: Boolean, default: true } })
const emit = defineEmits(['rename', 'reset', 'delete'])
const open = ref(false)
</script>
