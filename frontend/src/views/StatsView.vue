<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto space-y-5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/')" class="text-sm transition-colors" style="color:#71717a" onmouseover="this.style.color='white'" onmouseout="this.style.color='#71717a'">← Zpět</button>
          <h1 class="text-white font-bold text-lg">Statistiky</h1>
        </div>
        <button @click="confirmReset = true" class="text-xs transition-colors" style="color:#ef4444" onmouseover="this.style.color='#f87171'" onmouseout="this.style.color='#ef4444'">🗑 Reset</button>
      </div>

      <!-- Čísla — stats karty s barevným levým borderem -->
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div class="rounded-xl p-4 text-center border-l-4" style="background:#211d2f; border-left-color:#f59e0b; border-top:1px solid #2d2840; border-right:1px solid #2d2840; border-bottom:1px solid #2d2840">
          <p class="text-3xl font-bold" style="color:#fbbf24">{{ stats?.streak_days ?? 0 }}</p>
          <p class="text-xs mt-1" style="color:#71717a">streak dní 🔥</p>
        </div>
        <div class="rounded-xl p-4 text-center border-l-4" style="background:#211d2f; border-left-color:#22c55e; border-top:1px solid #2d2840; border-right:1px solid #2d2840; border-bottom:1px solid #2d2840">
          <p class="text-3xl font-bold" style="color:#4ade80">{{ stats?.total_learned ?? 0 }}</p>
          <p class="text-xs mt-1" style="color:#71717a">naučených karet</p>
        </div>
        <div class="rounded-xl p-4 text-center border-l-4" style="background:#211d2f; border-left-color:#7c3aed; border-top:1px solid #2d2840; border-right:1px solid #2d2840; border-bottom:1px solid #2d2840">
          <p class="text-3xl font-bold" style="color:#a78bfa">{{ stats?.total_reviews_today ?? 0 }}</p>
          <p class="text-xs mt-1" style="color:#71717a">hodnocení dnes</p>
        </div>
        <div class="rounded-xl p-4 text-center border-l-4" style="background:#211d2f; border-left-color:#3b82f6; border-top:1px solid #2d2840; border-right:1px solid #2d2840; border-bottom:1px solid #2d2840">
          <p class="text-3xl font-bold" style="color:#60a5fa">{{ stats?.total_reviews ?? 0 }}</p>
          <p class="text-xs mt-1" style="color:#71717a">hodnocení celkem</p>
        </div>
      </div>

      <!-- Streak kalendář (30 dní) -->
      <div class="rounded-xl p-4" style="background:#211d2f; border:1px solid #2d2840">
        <p class="text-xs uppercase tracking-wider mb-3" style="color:#52525b">Aktivita za 30 dní</p>
        <div class="grid grid-cols-10 gap-1.5">
          <div
            v-for="day in calendarDays"
            :key="day.date"
            class="aspect-square rounded-sm"
            :style="day.count > 0
              ? { background: '#7c3aed', opacity: Math.min(0.35 + day.count / maxCount * 0.65, 1) }
              : { background: '#2a2540' }"
            :title="`${day.date}: ${day.count} hodnocení`"
          />
        </div>
        <div class="flex justify-between text-xs mt-2" style="color:#3f3f60">
          <span>před 29 dny</span>
          <span>dnes</span>
        </div>
      </div>

      <!-- Sloupcový graf posledních 14 dní -->
      <div class="rounded-xl p-4" style="background:#211d2f; border:1px solid #2d2840">
        <p class="text-xs uppercase tracking-wider mb-4" style="color:#52525b">Hodnocení za 14 dní</p>
        <div class="flex items-end gap-1 h-24">
          <div
            v-for="day in last14"
            :key="day.date"
            class="flex-1 rounded-t-sm transition-all"
            style="background:linear-gradient(180deg,#a78bfa,#7c3aed); min-height:2px"
            :style="{ height: maxCount > 0 ? `${(day.count / maxCount) * 100}%` : '2px' }"
            :title="`${day.date}: ${day.count}`"
          />
        </div>
        <div class="flex justify-between text-xs mt-2" style="color:#3f3f60">
          <span>před 13 dny</span>
          <span>dnes</span>
        </div>
      </div>

      <!-- Confirm reset dialog -->
      <div v-if="confirmReset" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="rounded-2xl p-6 text-center space-y-4 mx-4" style="background:#211d2f; border:1px solid #2d2840">
          <p class="text-white font-semibold">Resetovat všechny statistiky?</p>
          <p class="text-sm" style="color:#71717a">Tato akce smaže veškerý postup učení a nelze ji vrátit.</p>
          <div class="flex gap-3 justify-center">
            <button @click="doReset" class="text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors" style="background:#991b1b" onmouseover="this.style.background='#b91c1c'" onmouseout="this.style.background='#991b1b'">Resetovat</button>
            <button @click="confirmReset = false" class="text-white px-4 py-2 rounded-lg text-sm" style="background:#2a2540">Zrušit</button>
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
