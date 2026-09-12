<template>
  <aside style="width:220px; background:#211d2f; border-right:1px solid #2d2840; display:flex; flex-direction:column; flex-shrink:0">
    <!-- Header -->
    <div style="padding:20px 16px; background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 100%)">
      <div style="font-size:15px; font-weight:800; color:white; letter-spacing:-0.3px">📚 FlashCards</div>
      <div style="font-size:10px; color:rgba(255,255,255,0.6); margin-top:2px">v0.9 · beta</div>
    </div>

    <!-- Desktop: Language tree -->
    <div v-if="!isMobile" style="flex:1; overflow-y:auto; padding:12px 8px">
      <LanguageItem
        v-for="lang in store.languages"
        :key="lang.id"
        :language="lang"
      />

      <!-- Přidat jazyk -->
      <div v-if="showAddLang" style="margin-top:8px; background:#2a2540; border-radius:10px; padding:12px">
        <input
          v-model="newLangName"
          placeholder="Název jazyka (např. Angličtina)"
          style="width:100%; background:#1a1625; border:1px solid #2d2840; border-radius:7px; padding:8px 10px; font-size:12px; color:white; outline:none; margin-bottom:8px"
          @keyup.enter="addLanguage"
          autofocus
        />
        <div style="display:flex; gap:6px; align-items:center; margin-bottom:8px">
          <input
            v-model="newLangEmoji"
            placeholder="🏳️"
            style="width:72px; background:#1a1625; border:1px solid #2d2840; border-radius:7px; padding:8px 10px; font-size:12px; color:white; outline:none"
          />
          <span style="font-size:11px; color:#52525b">vlajka/emoji</span>
        </div>
        <div style="display:flex; gap:6px">
          <button @click="addLanguage" style="background:#7c3aed; color:white; font-size:12px; font-weight:700; padding:7px 12px; border-radius:7px; border:none; flex:1; cursor:pointer">Přidat</button>
          <button @click="showAddLang = false" style="font-size:12px; color:#71717a; padding:7px 10px; border-radius:7px; border:none; background:transparent; cursor:pointer">Zrušit</button>
        </div>
      </div>
      <button v-else @click="showAddLang = true"
        style="width:100%; text-align:left; font-size:12px; color:#52525b; padding:7px 10px; margin-top:4px; border-radius:8px; border:none; background:transparent; cursor:pointer"
        @mouseover="$event.target.style.color='#a78bfa'"
        @mouseout="$event.target.style.color='#52525b'">
        + Přidat jazyk
      </button>
    </div>

    <!-- Mobil: prázdný flex-1 -->
    <div v-else style="flex:1" />

    <!-- Start / Zrušit tlačítko (jen desktop) -->
    <div v-if="!isMobile" style="padding:12px 8px; border-top:1px solid #2d2840">
      <button
        v-if="isStudying"
        @click="cancelStudy"
        style="width:100%; background:linear-gradient(135deg,#991b1b,#7f1d1d); color:white; font-size:14px; font-weight:800; padding:13px; border-radius:11px; border:none; cursor:pointer; letter-spacing:0.5px; text-transform:uppercase; box-shadow:0 4px 16px rgba(153,27,27,0.3)"
      >
        ✕ Zrušit lekci
      </button>
      <button
        v-else-if="store.selectedCount > 0"
        @click="startStudy"
        style="width:100%; background:linear-gradient(135deg,#7c3aed,#6d28d9); color:white; font-size:14px; font-weight:800; padding:13px; border-radius:11px; border:none; cursor:pointer; letter-spacing:0.5px; text-transform:uppercase; box-shadow:0 4px 20px rgba(124,58,237,0.4); transition:all 0.2s"
        @mouseover="$event.target.style.boxShadow='0 6px 30px rgba(124,58,237,0.6)'; $event.target.style.transform='translateY(-1px)'"
        @mouseout="$event.target.style.boxShadow='0 4px 20px rgba(124,58,237,0.4)'; $event.target.style.transform=''"
      >
        ▶ START ({{ store.selectedCount }})
      </button>
    </div>

    <!-- Nav -->
    <div style="padding:12px 8px; border-top:1px solid #2d2840; display:flex; gap:4px">
      <router-link to="/stats"
        style="flex:1; text-align:center; padding:8px 4px; border-radius:8px; font-size:11px; color:#52525b; background:#2a2540; text-decoration:none; transition:all 0.12s"
        @mouseover="$event.target.style.color='#a78bfa'"
        @mouseout="$event.target.style.color='#52525b'">
        📊 Stats
      </router-link>
      <button disabled style="flex:1; text-align:center; padding:8px 4px; border-radius:8px; font-size:11px; color:#3f3f46; background:#2a2540; border:none; cursor:not-allowed">
        ⚙️ Nast.
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLanguagesStore } from '../../stores/languages'
import { useStudyStore } from '../../stores/study'
import { api } from '../../api'
import LanguageItem from '../sidebar/LanguageItem.vue'

const store = useLanguagesStore()
const studyStore = useStudyStore()
const router = useRouter()
const route = useRoute()
const showAddLang = ref(false)
const newLangName = ref('')
const newLangEmoji = ref('')
const isMobile = ref(false)

function checkMobile() { isMobile.value = window.innerWidth < 768 }
onMounted(() => { checkMobile(); window.addEventListener('resize', checkMobile) })
onUnmounted(() => window.removeEventListener('resize', checkMobile))

const isStudying = computed(() =>
  route.path === '/study' && studyStore.cards.length > 0 && !studyStore.isFinished
)

function startStudy() {
  const ids = store.selectedCount > 0
    ? [...store.selectedLessonIds].join(',')
    : studyStore.currentLessonIds.join(',')
  router.push({ path: '/study', query: { lessons: ids, t: Date.now() } })
}

function cancelStudy() {
  studyStore.clearSession()
  router.push('/')
}

async function addLanguage() {
  if (!newLangName.value.trim()) return
  await api.createLanguage({ name: newLangName.value.trim(), emoji: newLangEmoji.value.trim() || '🌐' })
  newLangName.value = ''
  newLangEmoji.value = ''
  showAddLang.value = false
  await store.fetchDashboard()
}
</script>
