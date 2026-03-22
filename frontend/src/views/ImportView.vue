<template>
  <AppLayout>
    <div class="p-6 max-w-lg mx-auto space-y-6">
      <h1 class="text-white font-bold text-lg">Import karet</h1>

      <div
        class="border-2 border-dashed border-gray-700 rounded-xl p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors"
        :class="{ 'border-indigo-500 bg-indigo-950/20': isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="handleDrop"
        @click="fileInput.click()"
      >
        <p class="text-gray-500 text-4xl mb-3">📁</p>
        <p class="text-gray-400 text-sm">Přetáhni CSV nebo JSON soubor</p>
        <p class="text-gray-600 text-xs mt-1">nebo klikni pro výběr</p>
        <input ref="fileInput" type="file" accept=".csv,.json" class="hidden" @change="handleFile" />
      </div>

      <div class="bg-gray-900 rounded-lg p-4 text-xs text-gray-500 font-mono">
        <p class="text-gray-400 mb-1">CSV formát:</p>
        <p>front,back</p>
        <p>Hello,Ahoj</p>
      </div>

      <div v-if="result" class="bg-gray-900 rounded-lg p-4 text-sm">
        <p class="text-green-400">✓ Importováno: {{ result.imported }}</p>
        <p v-if="result.skipped > 0" class="text-yellow-500">⚠ Přeskočeno (duplicity): {{ result.skipped }}</p>
      </div>

      <button @click="$router.back()" class="text-gray-500 text-sm">← Zpět</button>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const route = useRoute()
const lessonId = route.params.lessonId
const isDragging = ref(false)
const result = ref(null)
const fileInput = ref(null)

async function importFile(file) {
  const { data } = await api.importCards(lessonId, file)
  result.value = data
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) importFile(file)
}

function handleFile(e) {
  const file = e.target.files[0]
  if (file) importFile(file)
}
</script>
