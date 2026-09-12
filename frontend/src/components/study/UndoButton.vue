<template>
  <button
    v-if="canUndo"
    @click="$emit('undo')"
    style="font-size:12px; color:#52525b; background:#211d2f; border:1px solid #2d2840; padding:5px 12px; border-radius:7px; cursor:pointer; transition:all 0.12s"
    @mouseover="$event.target.style.color='#a78bfa'; $event.target.style.borderColor='#4c1d95'"
    @mouseout="$event.target.style.color='#52525b'; $event.target.style.borderColor='#2d2840'"
  >
    ↩ Zpět
  </button>
</template>

<script setup>
defineProps({ canUndo: Boolean })
defineEmits(['undo'])
</script>
