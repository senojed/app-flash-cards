<template>
  <AppLayout>
    <div class="p-6 max-w-lg mx-auto space-y-6">
      <div class="flex items-center gap-3">
        <button @click="$router.back()" class="text-gray-400 hover:text-white text-sm">← Zpět</button>
        <h1 class="text-white font-bold text-lg">{{ isNew ? 'Nová karta' : 'Upravit kartu' }}</h1>
      </div>

      <div class="space-y-2">
        <label class="text-gray-400 text-xs uppercase tracking-wider">Přední strana</label>
        <textarea
          v-model="front"
          @input="scheduleTranslate"
          rows="3"
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white text-sm focus:outline-none focus:border-indigo-500 resize-none"
        />
        <MediaUpload v-if="cardId" :card-id="cardId" label="front" v-model="frontMedia" />
      </div>

      <div class="space-y-2">
        <label class="text-gray-400 text-xs uppercase tracking-wider">Zadní strana</label>
        <textarea
          v-model="back"
          rows="3"
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white text-sm focus:outline-none focus:border-indigo-500 resize-none"
        />
        <MediaUpload v-if="cardId" :card-id="cardId" label="back" v-model="backMedia" />
      </div>

      <div class="flex gap-3">
        <button @click="save" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg text-sm font-semibold flex-1">
          {{ isNew ? 'Přidat kartu' : 'Uložit' }}
        </button>
        <button v-if="!isNew" @click="deleteCard" class="bg-red-900 hover:bg-red-800 text-red-300 px-4 py-2 rounded-lg text-sm">
          Smazat
        </button>
        <button @click="$router.back()" class="text-gray-500 px-4 py-2 text-sm">Zrušit</button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import AppLayout from '../components/layout/AppLayout.vue'
import MediaUpload from '../components/cards/MediaUpload.vue'

const route = useRoute()
const router = useRouter()
const isNew = computed(() => !route.params.cardId)
const cardId = ref(route.params.cardId || null)
const lessonId = ref(route.params.lessonId)
const front = ref('')
const back = ref('')
const frontMedia = ref(null)
const backMedia = ref(null)
const targetLang = ref('cs')
let translateTimer = null

async function scheduleTranslate() {
  clearTimeout(translateTimer)
  if (!front.value.trim() || back.value) return
  translateTimer = setTimeout(async () => {
    try {
      const { data } = await api.translate(front.value, targetLang.value)
      if (!back.value) back.value = data.translation
    } catch {
      // překlad není dostupný
    }
  }, 1000)
}

async function save() {
  if (isNew.value) {
    await api.createCard({
      lesson_id: lessonId.value,
      fields: [
        { label: 'front', content: front.value },
        { label: 'back', content: back.value },
      ]
    })
  } else {
    await api.updateCard(cardId.value, {
      fields: [
        { label: 'front', content: front.value },
        { label: 'back', content: back.value },
      ]
    })
  }
  router.back()
}

async function deleteCard() {
  if (confirm('Smazat kartu?')) {
    await api.deleteCard(cardId.value)
    router.back()
  }
}

onMounted(async () => {
  const { data: dashboard } = await api.getDashboard()
  for (const lang of dashboard) {
    for (const lesson of lang.lessons) {
      if (lesson.id === lessonId.value) {
        targetLang.value = lang.target_lang
        break
      }
    }
  }

  if (!isNew.value) {
    const { data } = await api.getCards(lessonId.value)
    const card = data.find(c => c.id === cardId.value)
    if (card) {
      front.value = card.fields.find(f => f.label === 'front')?.content || ''
      back.value = card.fields.find(f => f.label === 'back')?.content || ''
    }
  }
})
</script>
