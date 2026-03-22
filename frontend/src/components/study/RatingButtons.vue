<template>
  <div class="flex gap-4 justify-center">
    <button @click="$emit('rate', 0)" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-xl font-semibold">✗ Nevím</button>
    <button @click="$emit('rate', 3)" class="bg-amber-500 hover:bg-amber-600 text-white px-6 py-3 rounded-xl font-semibold">~ Těžké</button>
    <button @click="$emit('rate', 4)" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold">✓ Umím</button>
    <button @click="$emit('rate', 5)" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold">⚡ Lehké</button>
  </div>
</template>

<script setup>
defineEmits(['rate'])
</script>
