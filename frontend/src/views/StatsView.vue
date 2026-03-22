<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/')" class="text-gray-400 hover:text-white text-sm">← Zpět</button>
          <h1 class="text-white font-bold text-lg">Statistiky</h1>
        </div>
        <button @click="confirmReset = true" class="text-red-500 hover:text-red-400 text-xs">🗑 Reset</button>
      </div>

      <!-- Čísla -->
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
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
        <div class="bg-gray-900 rounded-xl p-4 text-center">
          <p class="text-yellow-400 text-3xl font-bold">{{ stats?.total_reviews ?? 0 }}</p>
          <p class="text-gray-500 text-xs mt-1">hodnocení celkem</p>
        </div>
      </div>

      <!-- Streak kalendář (30 dní) -->
      <div class="bg-gray-900 rounded-xl p-4">
        <p class="text-gray-400 text-xs uppercase tracking-wider mb-3">Aktivita za 30 dní</p>
        <div class="grid grid-cols-10 gap-1.5">
          <div
            v-for="day in calendarDays"
            :key="day.date"
            class="aspect-square rounded-sm"
            :class="day.count > 0 ? 'bg-indigo-500' : 'bg-gray-800'"
            :title="`${day.date}: ${day.count} hodnocení`"
            :style="day.count > 0 ? { opacity: Math.min(0.4 + day.count / maxCount * 0.6, 1) } : {}"
          />
        </div>
        <div class="flex justify-between text-gray-600 text-xs mt-2">
          <span>před 29 dny</span>
          <span>dnes</span>
        </div>
      </div>

      <!-- Sloupcový graf posledních 14 dní -->
      <div class="bg-gray-900 rounded-xl p-4">
        <p class="text-gray-400 text-xs uppercase tracking-wider mb-4">Hodnocení za 14 dní</p>
        <div class="flex items-end gap-1 h-24">
          <div
            v-for="day in last14"
            :key="day.date"
            class="flex-1 bg-indigo-600 rounded-t-sm transition-all min-h-px"
            :style="{ height: maxCount > 0 ? `${(day.count / maxCount) * 100}%` : '2px' }"
            :title="`${day.date}: ${day.count}`"
          />
        </div>
        <div class="flex justify-between text-gray-600 text-xs mt-2">
          <span>před 13 dny</span>
          <span>dnes</span>
        </div>
      </div>

      <!-- Confirm reset dialog -->
      <div v-if="confirmReset" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="bg-gray-900 rounded-xl p-6 text-center space-y-4 mx-4">
          <p class="text-white font-semibold">Resetovat všechny statistiky?</p>
          <p class="text-gray-400 text-sm">Tato akce smaže veškerý postup učení a nelze ji vrátit.</p>
          <div class="flex gap-3 justify-center">
            <button @click="doReset" class="bg-red-700 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm">Resetovat</button>
            <button @click="confirmReset = false" class="bg-gray-700 text-white px-4 py-2 rounded-lg text-sm">Zrušit</button>
          </div>
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
const confirmReset = ref(false)

const calendarDays = computed(() => stats.value?.reviews_per_day ?? [])
const last14 = computed(() => calendarDays.value.slice(-14))
const maxCount = computed(() => Math.max(1, ...calendarDays.value.map(d => d.count)))

onMounted(async () => {
  const { data } = await api.getStats()
  stats.value = data
})

async function doReset() {
  confirmReset.value = false
  await api.resetStats()
  const { data } = await api.getStats()
  stats.value = data
}
</script>
