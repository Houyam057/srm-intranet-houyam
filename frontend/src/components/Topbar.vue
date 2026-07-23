<script setup>
import { ref } from 'vue' // <-- Correction 1 : Import de ref obligatoire
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useUiStore } from '../stores/ui.js'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const notifOpen = ref(false)
const messagesOpen = ref(false)

const choice = ref('')
const open = ref(false)

const choices = [
  "Profil",
  "Se Déconnecter"
]

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}

function selectChoice(item) {
  choice.value = item
  open.value = false
  if (item === "Profil") {
    router.push({ name: 'profil' })
  } else if (item === "Paramètres") {
    router.push({ name: 'settings' })
  } else if (item === "Se Déconnecter") {
    handleLogout()
  }
}
</script>

<template>
  <div class="topbar">
    <!-- Bouton hamburger : visible seulement en dessous de 1150px (voir main.css), ouvre le menu Sidebar en tiroir -->
    <button class="menu-toggle" @click="uiStore.toggleSidebar()" aria-label="Ouvrir le menu de navigation">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 6h18M3 12h18M3 18h18" />
      </svg>
    </button>

    <div class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round">
        <circle cx="11" cy="11" r="7" />
        <path d="M21 21l-4-4" />
      </svg>
      <input placeholder="Rechercher dans l'intranet..." />
      <kbd>Ctrl + K</kbd>
    </div>
    
    <div class="top-actions">
      <!-- Avant : juste une icone decorative avec un badge "3" en dur, aucune action au clic.
           Maintenant : ouvre un petit menu honnete (pas de fausses notifications) -->
      <div class="ic-btn" style="position:relative;" @click.stop="notifOpen = !notifOpen; messagesOpen = false; open = false">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.7 21a2 2 0 0 1-3.4 0" />
        </svg>
        <div v-if="notifOpen" class="dropdown__list" style="position:absolute;top:100%;right:0;z-index:10;min-width:220px;">
          <div class="dropdown__option" style="cursor:default;">Aucune notification pour le moment</div>
        </div>
      </div>

      <div class="ic-btn" style="position:relative;" @click.stop="messagesOpen = !messagesOpen; notifOpen = false; open = false">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="5" width="18" height="14" rx="2" />
          <path d="M3 7l9 6 9-6" />
        </svg>
        <div v-if="messagesOpen" class="dropdown__list" style="position:absolute;top:100%;right:0;z-index:10;min-width:220px;">
          <div class="dropdown__option" style="cursor:default;">Aucun message pour le moment</div>
        </div>
      </div>

      <div class="divider"></div>
      
      <div class="user" @click="open = !open; notifOpen = false; messagesOpen = false" style="cursor:pointer; position: relative;">
        <div class="av">{{ authStore.userInitials }}</div>
        <div>
          <b>{{ authStore.userName || 'Utilisateur' }}</b>
          <span>{{ authStore.user?.username || '' }}</span>
        </div>
        <svg class="chev" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 9l6 6 6-6" />
        </svg>

        <div v-if="open" class="dropdown__list" style="position: absolute; top: 100%; right: 0; z-index: 10;">
  <button 
    v-for="item in choices" 
    :key="item" 
    type="button" 
    :class="['dropdown__option', { 'is-logout': item === 'Se Déconnecter' }]"
    @click.stop="selectChoice(item)"
  >
    <b>{{ item }}</b>
  </button>
</div>
      </div> </div>
  </div>
</template>


<style scoped>
.dropdown__option.is-logout{
  color: #d32f2f; /* Texte rouge */
}
.dropdown__option.is-logout:hover {
  background-color: var(--red); /* Fond rouge très clair (optionnel) */
  color: white; /* Texte blanc au survol (optionnel) */
}
</style>