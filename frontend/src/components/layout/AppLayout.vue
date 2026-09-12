<template>
  <div style="display:flex; height:100vh; background:#1a1625; color:#f0f0f8; overflow:hidden; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
    <!-- Desktop sidebar -->
    <AppSidebar v-if="!isMobile" />

    <!-- Mobilní overlay menu -->
    <div v-if="isMobile && menuOpen" class="fixed inset-0 z-40 flex">
      <div style="width:220px; background:#211d2f; height:100%; overflow-y:auto">
        <AppSidebar @close="menuOpen = false" />
      </div>
      <div class="flex-1 bg-black/50" @click="menuOpen = false" />
    </div>

    <!-- Main content -->
    <div style="flex:1; display:flex; flex-direction:column; overflow:hidden">
      <AppTopbar v-if="isMobile" @menu="menuOpen = true" />
      <main style="flex:1; overflow:auto; padding:24px">
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
