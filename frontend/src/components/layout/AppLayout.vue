<template>
  <div class="flex h-screen bg-gray-950 text-gray-100">
    <!-- Desktop sidebar -->
    <AppSidebar v-if="!isMobile" />

    <!-- Mobilní overlay menu -->
    <div v-if="isMobile && menuOpen" class="fixed inset-0 z-40 flex">
      <div class="w-72 bg-gray-900 h-full overflow-y-auto">
        <AppSidebar @close="menuOpen = false" />
      </div>
      <div class="flex-1 bg-black/50" @click="menuOpen = false" />
    </div>

    <div class="flex flex-col flex-1 overflow-hidden">
      <AppTopbar v-if="isMobile" @menu="menuOpen = true" />
      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'

const isMobile = ref(false)
const menuOpen = ref(false)

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => { checkMobile(); window.addEventListener('resize', checkMobile) })
onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>
