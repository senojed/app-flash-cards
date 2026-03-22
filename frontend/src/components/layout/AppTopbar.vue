<template>
  <header class="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between">
    <button @click="$emit('menu')" class="text-gray-400 text-xl">☰</button>
    <span class="text-indigo-400 font-bold text-sm">FlashCards</span>
    <span class="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-xs">👤</span>
  </header>
</template>

<script setup>
defineEmits(['menu'])
</script>
