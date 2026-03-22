<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">Přejmenovat</p>
        <input
          v-model="value"
          @keyup.enter="$emit('confirm', value)"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500"
          autofocus
        />
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="$emit('confirm', value)" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Uložit</button>
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
