<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NAV_DIRECTIONS } from '../data/directions.js'
import { Info,Phone  } from 'lucide-vue-next'
import logo from '../assets/logo.png'
import { useUiStore } from '../stores/ui.js'
const route = useRoute()
const router = useRouter()
const uiStore = useUiStore()

// équivalent du subDir.classList.toggle('open') du mockup
const subOpen = ref(false)

const isAccueil = computed(() => route.name === 'accueil')
const isDirectionsArea = computed(() =>
  route.name === 'mesdirections' || route.name === 'direction-comm' || route.name === 'direction-generique'
)
const isHelpDesk = computed(() => route.name === 'helpdesk')
const isFlashInfo = computed(() => route.name === 'flashinfo')
const isNotreSociete = computed(() => route.name === 'notre-societe')
const isApps = computed(() => ['apps', 'sap', 'sap-bi', 'odoo'].includes(route.name))
const isFormation = computed(() => route.name==='formations-competences' )
const isNosMetiers = computed(() => route.name === 'nos-metiers')
const isProfil = computed(() => route.name === 'profil')
const isDocuments = computed(() => route.name === 'documents')

function goToFormation(){
  router.push({name:'formations-competences'})
}
function goToFlashInfo() {
  router.push({ name: 'flashinfo' })
}

function goToApps(){
  router.push({name : 'apps'})
}

function HelpDesk() {
  router.push({ name: 'helpdesk' })
}

function toggleDirections() {
  subOpen.value = !subOpen.value
  router.push({ name: 'mesdirections' })
}

function goToDirection(key) {
  if (key === 'comm') {
    // "Communication Externe & Marketing" a une page dédiée détaillée dans la maquette
    router.push({ name: 'direction-comm' })
    return
  }
  // Toutes les autres directions (y compris "dsi", votre direction) utilisent le template générique
  router.push({ name: 'direction-generique', params: { key } })
}

function goToWebsite() {
  router.push({ name: 'notre-societe' })
}

function goToNosMetiers() {
  router.push({ name: 'nos-metiers' })
}

function goToProfil() {
  router.push({ name: 'profil' })
}

function goToDocuments() {
  router.push({ name: 'documents' })
}
</script>

<template>
  <!-- sidebar--open : classe ajoutee seulement sous 1150px, pour afficher le menu en tiroir (voir main.css).
       @click.capture ferme le tiroir des qu'on choisit un lien, pour ne pas rester ouvert par-dessus la page -->
  <aside class="sidebar" :class="{ 'sidebar--open': uiStore.sidebarOpen }" @click.capture="uiStore.closeSidebar()">
    <div class="brand">
      <!-- Remplacez par le vrai logo SRM-TTA (SVG/PNG) -->
      <img :src="logo" alt="Logo SRM-TTA" class="logo" />
    </div>

    <div class="nav-item nav-accueil" :class="{ active: isAccueil }" @click="router.push({ name: 'accueil' })">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg>
      <span>Accueil</span>
    </div>
    
    <div class="nav-item" :class="{ active: isNotreSociete }" @click="goToWebsite">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 21h18M5 21V7l7-4 7 4v14"/>
        <path d="M9 12h.01M15 12h.01M9 16h6"/>
      </svg>
      <span>Notre société</span>
    </div>

    <div class="nav-item" :class="{ active: isNosMetiers }" @click="goToNosMetiers">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/></svg>
      <span>Nos métiers</span>
    </div>

    <div class="nav-item" :class="{ active: isFlashInfo }" @click="goToFlashInfo">
      <Info />
      <span>Flash Info</span>
    </div>

    <div class="nav-item nav-dir" :class="{ active: isDirectionsArea }" @click="toggleDirections">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg>
      <span>Nos Directions</span>
    </div>


    <div class="nav-item" :class="{ active: isProfil }" @click="goToProfil">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="14" rx="2"/><path d="M8 6V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1"/><circle cx="9" cy="12" r="2"/><path d="M6 17c.8-1.5 4.2-1.5 6 0M15 11h3M15 15h3"/></svg>
      <span>Mon Espace Collaborateur</span>
    </div>
    <div class="nav-item" :class="{ active: isDocuments }" @click="goToDocuments">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/></svg>
      <span>Documents &amp; Procédures</span>
    </div>
    <div class="nav-item" :class="{ active: isApps }" @click="goToApps">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
      <span>Outils &amp; Applications</span>
    </div>
    <div class="nav-item" :class="{active: isFormation }" @click="goToFormation">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/></svg>
      <span>Formation &amp; Compétences</span>
    </div>
    <div class="nav-item nav-help" :class="{ active: isHelpDesk }" @click="HelpDesk">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1v-5h3zM3 19a2 2 0 0 0 2 2h1v-5H3z"/></svg>
      <span>HelpDesk</span>
    </div>

    <div class="side-help">
      <div class="h-ic">
        <Phone />
      </div>
      <div>
        <!--<b>Besoin d'aide ?</b>-->
        <b style="font-size:11.5px;">Contactez le support IT</b>
        <div class="num">0801 000 042</div>
        <div class="bar"></div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.logo {
  width: 186px;
  height: 160px;
  object-fit: contain;
}
</style>