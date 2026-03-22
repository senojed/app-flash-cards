<template>
  <AppLayout>
    <div class="p-6 max-w-2xl mx-auto space-y-6">
      <h1 class="text-white font-bold text-lg">Statistiky</h1>

      <div class="grid grid-cols-3 gap-4">
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-indigo-400 text-3xl font-bold">{{ stats?.streak_days ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">streak dní 🔥</p>
        </div>
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-green-400 text-3xl font-bold">{{ stats?.total_learned ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">naučených karet</p>
        </div>
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-white text-3xl font-bold">{{ stats?.total_reviews_today ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">hodnocení dnes</p>
        </div>
      </div>

      <div class="bg-gray-900 rounded-xl p-4">
        <p class="text-gray-400 text-xs uppercase tracking-wider mb-4">Přesnost za 7 dní</p>
        <div class="flex items-end gap-2 h-24">
          <div
            v-for="(val, i) in accuracy"
            :key="i"
            class="flex-1 bg-indigo-600 rounded-t-sm transition-all"
            :style="{ height: `${val * 100}%` }"
            :title="`${Math.round(val * 100)}%`"
          />
        </div>
        <div class="flex justify-between text-gray-600 text-xs mt-2">
          <span>před 6 dny</span>
          <span>dnes</span>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'

const stats = ref(null)
const accuracy = computed(() => stats.value?.accuracy_7days ?? Array(7).fill(0))

onMounted(async () => {
  const { data } = await api.getStats()
  stats.value = data
})
</script>
