<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">Upravit jazyk</p>
        <div class="space-y-2">
          <label class="text-gray-400 text-xs">Název</label>
          <input v-model="name" @keyup.enter="confirm" autofocus
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500" />
        </div>
        <div class="space-y-2">
          <label class="text-gray-400 text-xs">Emoji / zkratka</label>
          <input v-model="emoji" @keyup.enter="confirm"
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500" />
        </div>
        <div class="space-y-2">
          <label class="text-gray-400 text-xs">Jazyk karty (BCP-47, např. en, de, fr)</label>
          <input v-model="sourceLang" @keyup.enter="confirm" placeholder="en"
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500" />
        </div>
        <div class="space-y-2">
          <label class="text-gray-400 text-xs">Procvičování</label>
          <select v-model="directionMode"
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500">
            <option value="front_to_back">Přední → Zadní</option>
            <option value="back_to_front">Zadní → Přední</option>
            <option value="random">Náhodně (obě strany)</option>
          </select>
        </div>
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="confirm" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm">Uložit</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ initialName: String, initialEmoji: String, initialSourceLang: String, initialDirectionMode: String })
const emit = defineEmits(['confirm', 'cancel'])
const name = ref(props.initialName || '')
const emoji = ref(props.initialEmoji || '')
const sourceLang = ref(props.initialSourceLang || 'en')
const directionMode = ref(props.initialDirectionMode || 'front_to_back')

function confirm() {
  emit('confirm', { name: name.value, emoji: emoji.value, source_lang: sourceLang.value, direction_mode: directionMode.value })
}
</script>
