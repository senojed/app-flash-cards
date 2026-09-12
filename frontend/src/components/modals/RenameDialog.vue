<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="rounded-2xl p-6 w-80 space-y-4" style="background:#211d2f; border:1px solid #2d2840">
        <p class="text-white font-semibold">Přejmenovat</p>
        <input
          v-model="value"
          @keyup.enter="$emit('confirm', value)"
          class="w-full rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-1"
          style="background:#1a1625; border:1px solid #2d2840; --tw-ring-color:#7c3aed"
          autofocus
        />
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="px-4 py-2 text-sm transition-colors" style="color:#71717a" onmouseover="this.style.color='white'" onmouseout="this.style.color='#71717a'">Zrušit</button>
          <button @click="$emit('confirm', value)" class="text-white px-4 py-2 rounded-lg text-sm font-semibold" style="background:#7c3aed">Uložit</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ initialValue: String })
defineEmits(['confirm', 'cancel'])
const value = ref(props.initialValue || '')
</script>
