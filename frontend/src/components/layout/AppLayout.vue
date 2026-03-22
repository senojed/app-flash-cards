<template>
  <div class="flex bg-gray-950 text-gray-100 gap-3 h-screen p-3">
    <!-- Desktop sidebar -->
    <AppSidebar v-if="!isMobile" />

    <!-- Mobilní overlay menu -->
    <div v-if="isMobile && menuOpen" class="fixed inset-0 z-40 flex">
      <div class="w-72 bg-gray-900 h-full overflow-y-auto">
        <AppSidebar @close="menuOpen = false" />
      </div>
      <div class="flex-1 bg-black/50" @click="menuOpen = false" />
    </div>

    <div class="flex flex-col flex-1 overflow-hidden rounded-2xl bg-gray-900 border border-gray-800">
      <AppTopbar v-if="isMobile" @menu="menuOpen = true" />
      <main class="flex-1 overflow-auto" style="padding:24px">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'
import { useLanguagesStore } from '../../stores/languages'

const isMobile = ref(false)
const menuOpen = ref(false)
const langStore = useLanguagesStore()

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  if (langStore.languages.length === 0) langStore.fetchDashboard()
})
onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>
