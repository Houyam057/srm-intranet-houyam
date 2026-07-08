<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { DIRS, DIRECTION_GROUPS } from '../data/directions.js'
import { odooApi } from '../api/odoo.js'

const router = useRouter()
const apiDirections = ref({})

function dir(key) {
  return apiDirections.value[key] || DIRS[key]
}

function openMine() {
  // Dans la maquette d'origine, "Mon espace" (DSI) ouvre aussi le template générique
  router.push({ name: 'direction-generique', params: { key: 'dsi' } })
}

function openDirection(key) {
  router.push({ name: 'direction-generique', params: { key } })
}

function initials(fullName) {
  return fullName.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
}

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
  <div class="page page-mesdirections show">
    <div class="crumbs">Accueil <span class="sep">›</span> <span class="cur">Nos Directions</span></div>

    <div class="card-h" style="margin-bottom:0"><h3 style="font-size:20px">Nos Directions</h3></div>

    <!-- ACCESS BANNER -->
    <div class="access-banner">
      <div class="lk">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>
      </div>
      <div>
        <b>Accès personnalisé selon votre profil</b>
        <p>Vous accédez à votre direction de rattachement. Les autres espaces sont affichés en lecture restreinte.</p>
      </div>
      <div class="who">Connectée en tant que<b>Sara BERRAADI · DSI &amp; Transformation Digitale</b></div>
    </div>

    <!-- MY SPACE -->
    <div class="card card-pad myspace" style="cursor:pointer" @click="openMine">
      <div class="big-ic">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>
      </div>
      <div>
        <span class="tag">MON ESPACE</span>
        <h3>{{ dir('dsi').name }}</h3>
        <p>Responsable : {{ dir('dsi').mgr }} · {{ dir('dsi').pole }} · {{ dir('dsi').eff }} collaborateur</p>
      </div>
      <button class="btn-primary" style="margin-left:auto" @click.stop="openMine">
        Accéder à mon espace
        <svg viewBox="0 0 24 24" width="16" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </button>
    </div>

    <!-- DIRECTION GÉNÉRALE -->
    <div class="dg-top">
      <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/></svg></div>
      <div><h3>Direction Générale</h3><p>Direction de tête de la SRM-TTA · {{ dir('dg').eff }} collaborateurs</p></div>
      <div class="mgr">Directrice Générale<b>{{ dir('dg').mgr }}</b></div>
    </div>

    <!-- GROUPES / PÔLES -->
    <div class="dgroup" v-for="group in DIRECTION_GROUPS" :key="group.title">
      <div class="gh">
        <span class="chip">{{ group.chip }}</span>
        <h3>{{ group.title }}</h3>
        <span class="mgr">Responsable : {{ group.mgr }}</span>
      </div>
      <div class="dcards">
        <div
          v-for="c in group.cards"
          :key="c.key"
          class="dcard clickable"
          :class="{ locked: c.locked, mine: c.mine }"
          @click="openDirection(c.key)"
        >
          <span v-if="c.mine" class="tagme">MOI</span>
          <div class="ic">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/></svg>
          </div>
          <h4>{{ dir(c.key).name }}</h4>
          <div class="mgr"><span class="av">{{ initials(dir(c.key).mgr) }}</span>{{ dir(c.key).mgr }}</div>
          <div class="foot">
            <span class="cnt">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="3"/></svg>{{ c.eff }}
            </span>
            <span v-if="c.locked" class="lock">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Restreint
            </span>
            <span v-else class="open">
              Ouvrir
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
