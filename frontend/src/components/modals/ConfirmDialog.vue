<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-80 space-y-4">
        <p class="text-white font-semibold">{{ title }}</p>
        <p class="text-gray-400 text-sm">{{ message }}</p>
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="text-gray-400 px-4 py-2 text-sm">Zrušit</button>
          <button @click="$emit('confirm')" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm">
            {{ confirmLabel }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({ title: String, message: String, confirmLabel: { type: String, default: 'Smazat' } })
defineEmits(['confirm', 'cancel'])
</script>
