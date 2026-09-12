<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="rounded-2xl p-6 w-80 space-y-4" style="background:#211d2f; border:1px solid #2d2840">
        <p class="text-white font-semibold">{{ title }}</p>
        <p class="text-sm" style="color:#71717a">{{ message }}</p>
        <div class="flex gap-3 justify-end">
          <button @click="$emit('cancel')" class="px-4 py-2 text-sm transition-colors" style="color:#71717a" onmouseover="this.style.color='white'" onmouseout="this.style.color='#71717a'">Zrušit</button>
          <button @click="$emit('confirm')" class="text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors" style="background:#991b1b" onmouseover="this.style.background='#b91c1c'" onmouseout="this.style.background='#991b1b'">
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
