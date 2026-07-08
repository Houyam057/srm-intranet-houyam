<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { DIRS } from '../data/directions.js'
import { odooApi } from '../api/odoo.js'

const props = defineProps({
  key: { type: String, required: true }
})
const router = useRouter()
const apiDirections = ref({})

// équivalent de : const d = DIRS[key]; document.getElementById('gdName')... du mockup
const direction = computed(() => apiDirections.value[props.key] || DIRS[props.key] || { name: 'Direction inconnue', mgr: '—', pole: '—', eff: '—' })

const notes = [
  { text: 'Note de service interne de la direction', date: '26/06/2026' },
  { text: 'Procédure mise à jour — circuit de validation', date: '22/06/2026' },
  { text: 'Organisation des horaires — période estivale', date: '18/06/2026' }
]

const projets = [
  { title: 'Projet structurant n°1', sub: "Phase d'exécution", pct: 70 },
  { title: 'Chantier d\'amélioration continue', sub: 'En cours de déploiement', pct: 45 }
]

const docs = [
  { name: 'Organigramme de la direction', meta: 'PDF · 0.8 Mo', type: 'pdf' },
  { name: 'Procédures internes', meta: 'DOCX · 1.4 Mo', type: 'doc' },
  { name: 'Présentation de la direction', meta: 'PPTX · 3.1 Mo', type: 'ppt' }
]

onMounted(async () => {
  try {
    const response = await odooApi.get('/api/directions')
    const directions = response.data?.data?.directions || []
    apiDirections.value = directions.reduce((all, item) => {
      if (!item.code) return all
      all[item.code.toLowerCase()] = {
        name: item.name,
        mgr: item.manager_name || '—',
        pole: item.pole_name || '—',
        eff: item.employee_count ?? '—'
      }
      return all
    }, {})
  } catch {
    // Keep local mock data when Odoo is not reachable.
  }
})
</script>

<template>
  <div class="page page-dirgen show">
    <div class="crumbs">
      Accueil <span class="sep">›</span>
      <span class="lnk" @click="router.push({ name: 'mesdirections' })">Nos Directions</span>
      <span class="sep">›</span>
      <span class="cur">{{ direction.name }}</span>
    </div>

    <div class="gd-hero">
      <div class="kicker">Direction</div>
      <h1>{{ direction.name }}</h1>
      <div class="tri-h"></div>
      <div class="gd-meta">
        <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/></svg>Responsable : <b>{{ direction.mgr }}</b></div>
        <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/></svg>Rattachement : <b>{{ direction.pole }}</b></div>
        <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg><b>{{ direction.eff }}</b> collaborateur(s)</div>
      </div>
    </div>

    <div class="gd-note">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>
      Page type de la maquette — le contenu réel (notes, projets, documents, équipe) sera propre à chaque direction et visible selon le profil de l'utilisateur.
    </div>

    <div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:20px">
      <div class="card card-pad">
        <div class="card-h"><h3>Notes de service</h3><span class="see">Voir tout</span></div>
        <div class="note" v-for="(n, i) in notes" :key="i">
          <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg></div>
          <div class="b"><p>{{ n.text }}</p></div>
          <div class="date">{{ n.date }}</div>
        </div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Projets en cours</h3><span class="see">Voir tout</span></div>
        <div class="proj" v-for="(p, i) in projets" :key="i">
          <div class="top">
            <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20h20M4 20V9l5 3V9l5 3V6l6 4v10"/></svg></div>
            <div style="flex:1"><h4>{{ p.title }}</h4><div class="sub">{{ p.sub }}</div></div>
          </div>
          <div class="bar"><i :style="{ width: p.pct + '%' }"></i></div><div class="pct">{{ p.pct }}%</div>
        </div>
        <div class="btn-ghost" style="border-style:solid">Tous les projets <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Documents utiles</h3><span class="see">Voir tout</span></div>
        <div class="grid" style="gap:12px">
          <div class="doc" v-for="(d, i) in docs" :key="i">
            <div class="ft" :class="'ft-' + d.type">{{ d.type.toUpperCase() }}</div>
            <div class="b"><b>{{ d.name }}</b><span>{{ d.meta }}</span></div>
            <div class="dl"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
