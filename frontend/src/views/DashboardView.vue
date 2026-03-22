<template>
  <AppLayout>
    <div class="flex items-center justify-center h-full text-gray-600 text-sm">
      <div class="text-center">
        <p class="text-4xl mb-4">📚</p>
        <p>Vyber lekce v postranním panelu a klikni Začít.</p>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import { useLanguagesStore } from '../stores/languages'
import AppLayout from '../components/layout/AppLayout.vue'

const store = useLanguagesStore()
onMounted(() => store.fetchDashboard())
</script>
