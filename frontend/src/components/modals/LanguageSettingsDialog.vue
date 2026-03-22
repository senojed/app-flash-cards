<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">Nastavení jazyka</p>
        <div class="space-y-2">
          <label class="text-gray-400 text-xs">Procvičování</label>
          <select v-model="directionMode"
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500">
            <option value="random">Náhodně (obě strany)</option>
            <option value="front_to_back">Přední → Zadní</option>
            <option value="back_to_front">Zadní → Přední</option>
          </select>
        </div>
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="$emit('confirm', { direction_mode: directionMode })" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Uložit</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ initialDirectionMode: String })
defineEmits(['confirm', 'cancel'])
const directionMode = ref(props.initialDirectionMode || 'random')
</script>
