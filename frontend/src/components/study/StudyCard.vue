<template>
  <div class="relative flex items-center justify-center">
    <Transition :name="slideClass" mode="out-in">
      <div
        :key="card.card_id + card.direction"
        class="bg-gradient-to-br from-indigo-950 to-gray-900 border border-indigo-800 rounded-2xl p-8 text-center w-80 cursor-pointer select-none"
        @click="!revealed && emit('reveal')"
      >
        <p class="text-indigo-300 text-xs uppercase tracking-widest mb-4">
          {{ card.direction === 'front_to_back' ? 'Přelož' : 'Co to je?' }}
        </p>
        <p class="text-white text-3xl font-bold mb-4">{{ card.front }}</p>

        <button @click.stop="speak(card.front, sourceLang)" class="text-indigo-400 text-sm mb-4">🔊</button>

        <Transition name="fade">
          <div v-if="revealed" class="mt-4 border-t border-indigo-800 pt-4">
            <p class="text-gray-300 text-2xl">{{ card.back }}</p>
            <img v-if="card.back_image" :src="`/media/${card.back_image}`"
                 class="mt-3 rounded-lg max-h-32 mx-auto" />
            <button @click.stop="speak(card.back)" class="text-indigo-400 text-sm mt-2">🔊</button>
          </div>
        </Transition>

        <p v-if="!revealed" class="text-gray-600 text-xs mt-6">klikni pro odhalení</p>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const props = defineProps({ card: Object, revealed: Boolean, slideClass: String, sourceLang: { type: String, default: '' } })
const emit = defineEmits(['reveal'])

function speak(text, lang) {
  if (!text || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
  const utt = new SpeechSynthesisUtterance(text)
  if (lang) utt.lang = lang
  window.speechSynthesis.speak(utt)
}
</script>

<style scoped>
.slide-left-enter-active, .slide-left-leave-active,
.slide-right-enter-active, .slide-right-leave-active { transition: all 0.3s ease; }
.slide-left-leave-to { transform: translateX(-100%); opacity: 0; }
.slide-right-leave-to { transform: translateX(100%); opacity: 0; }
.slide-left-enter-from, .slide-right-enter-from { transform: translateX(0); opacity: 1; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
