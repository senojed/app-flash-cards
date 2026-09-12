<template>
  <div style="position:relative; display:flex; align-items:center; justify-content:center; width:100%; max-width:500px">
    <Transition :name="slideClass" mode="out-in">
      <div
        :key="card.card_id + card.direction"
        style="width:100%; background:#211d2f; border:2px solid #2d2840; border-radius:24px; padding:44px 50px; text-align:center; cursor:pointer; position:relative; z-index:1; box-shadow:0 8px 40px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.04); transition:all 0.2s"
        @click="!revealed && emit('reveal')"
        @mouseover="!revealed && ($event.currentTarget.style.borderColor='#4c1d95') && ($event.currentTarget.style.boxShadow='0 12px 60px rgba(0,0,0,0.5),0 0 0 1px rgba(124,58,237,0.2)') && ($event.currentTarget.style.transform='translateY(-3px)')"
        @mouseout="$event.currentTarget.style.borderColor='#2d2840'; $event.currentTarget.style.boxShadow='0 8px 40px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.04)'; $event.currentTarget.style.transform=''"
      >
        <!-- Badge -->
        <div style="display:inline-flex; align-items:center; gap:6px; background:#2d2840; border:1px solid #3d3860; border-radius:99px; padding:4px 12px; font-size:10px; color:#a78bfa; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:22px">
          🔤 {{ card.direction === 'front_to_back' ? 'Přelož' : 'Co to je?' }}
        </div>

        <!-- Front text -->
        <p style="font-size:50px; font-weight:800; color:white; letter-spacing:-2px; line-height:1; margin-bottom:12px">{{ card.front }}</p>

        <!-- TTS front -->
        <button @click.stop="speak(card.front, sourceLang)"
                style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:#4c1d95; cursor:pointer; padding:6px 14px; border-radius:99px; background:#2d2840; border:1px solid #3d3860; margin-bottom:28px; transition:all 0.15s; font-weight:600"
                @mouseover="$event.target.style.color='#a78bfa'; $event.target.style.borderColor='#4c1d95'; $event.target.style.background='#2a1f45'"
                @mouseout="$event.target.style.color='#4c1d95'; $event.target.style.borderColor='#3d3860'; $event.target.style.background='#2d2840'">
          🔊 Přehrát
        </button>

        <!-- Divider -->
        <div style="height:1px; background:#2d2840; margin-bottom:24px"></div>

        <!-- Back + fade -->
        <Transition name="fade">
          <div v-if="revealed">
            <p style="font-size:34px; color:#c4b5fd; font-weight:600; letter-spacing:-0.5px; margin-bottom:12px">{{ card.back }}</p>
            <img v-if="card.back_image" :src="`/media/${card.back_image}`"
                 style="margin-top:12px; border-radius:8px; max-height:128px; display:block; margin-left:auto; margin-right:auto" />
            <button @click.stop="speak(card.back, targetLang)"
                    style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:#4c1d95; cursor:pointer; padding:5px 12px; border-radius:99px; background:#2d2840; border:1px solid #3d3860; transition:all 0.15s; font-weight:600"
                    @mouseover="$event.target.style.color='#a78bfa'; $event.target.style.borderColor='#4c1d95'; $event.target.style.background='#2a1f45'"
                    @mouseout="$event.target.style.color='#4c1d95'; $event.target.style.borderColor='#3d3860'; $event.target.style.background='#2d2840'">
              🔊 Přehrát
            </button>
          </div>
        </Transition>

        <p v-if="!revealed" style="font-size:11px; color:#3f3f60; margin-top:24px">klikni pro odhalení</p>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const props = defineProps({ card: Object, revealed: Boolean, slideClass: String, sourceLang: { type: String, default: '' }, targetLang: { type: String, default: '' } })
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
