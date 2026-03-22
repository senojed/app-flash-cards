<template>
  <button
    v-if="canUndo"
    @click="$emit('undo')"
    class="text-gray-500 hover:text-gray-300 text-xs flex items-center gap-1"
  >
    ↩ Zpět
  </button>
</template>

<script setup>
defineProps({ canUndo: Boolean })
defineEmits(['undo'])
</script>
