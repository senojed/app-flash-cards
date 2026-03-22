<template>
  <div class="flex items-center gap-2">
    <input ref="fileInput" type="file" :accept="acceptTypes" class="hidden" @change="handleFile" />
    <button
      type="button"
      @click="fileInput.click()"
      class="text-xs text-gray-500 hover:text-gray-300 border border-gray-700 rounded px-2 py-1"
    >
      {{ currentPath ? '🔄 Změnit' : '📎 Přidat' }} {{ label === 'front' ? 'přední' : 'zadní' }} media
    </button>
    <span v-if="currentPath" class="text-xs text-gray-600 truncate max-w-32">{{ fileName }}</span>
    <button v-if="currentPath" @click="remove" class="text-xs text-red-600 hover:text-red-400">✕</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { api } from '../../api'

const props = defineProps({
  cardId: String,
  label: String,
  modelValue: String,
})
const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const acceptTypes = 'image/png,image/jpeg,image/webp,audio/mpeg,audio/ogg'
const currentPath = computed(() => props.modelValue)
const fileName = computed(() => currentPath.value?.split('/').pop() ?? '')

async function handleFile(e) {
  const file = e.target.files[0]
  if (!file || !props.cardId) return
  const { data } = await api.uploadMedia(props.cardId, props.label, file)
  emit('update:modelValue', data.path)
}

function remove() {
  emit('update:modelValue', null)
}
</script>
