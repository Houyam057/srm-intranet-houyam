<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { odooApi } from '../api/odoo.js'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const directions = ref([])
const loading = ref(true)

const directionP = computed(() => directions.value.find(d => d.code === 'DG') || null)

const userDirectionId = computed(() => auth.user?.direction_id || 0)

function isMyDirection(d) {
  return userDirectionId.value && d.id === userDirectionId.value
}

const groups = computed(() => {
  const poleMap = {}
  const poleManagerMap = {}
  for (const d of directions.value) {
    if (d.code === 'DG') continue
    const pole = d.pole_name || 'Sans pôle'
    if (!poleMap[pole]) {
      poleMap[pole] = []
      poleManagerMap[pole] = d.pole_manager_name || '—'
    }
    poleMap[pole].push(d)
  }
  return Object.entries(poleMap).map(([pole, items]) => ({
    pole,
    title: items[0]?.name || pole,
    mgr: poleManagerMap[pole],
    items
  }))
})

function openDirection(id) {
  router.push({ name: 'direction-generique', params: { key: String(id) } })
}

function initials(name) {
  return (name || '').split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
}

onMounted(async () => {
  try {
    const response = await odooApi.get('/api/directions')
    directions.value = response.data?.data?.directions || []
  } catch {
    directions.value = []
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page page-mesdirections show">
    <div class="crumbs">Accueil <span class="sep">›</span> <span class="cur">Nos Directions</span></div>

    <div class="card-h" style="margin-bottom:0"><h3 style="font-size:20px">Nos Directions</h3></div>

    <!-- ACCESS BANNER -->
    <!--<div class="access-banner">
      <div class="lk">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>
      </div>
      <div>
        <b>Accès personnalisé selon votre profil</b>
        <p>Vous accédez à votre direction de rattachement. Les autres espaces sont affichés en lecture restreinte.</p>
      </div>
    </div>
  -->
    <!-- LOADING -->
    <div v-if="loading" style="text-align:center;padding:40px">Chargement des directions...</div>

    <template v-else>
      <!-- DIRECTION GÉNÉRALE -->
      <div v-if="directionP" class="dg-top">
        <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/></svg></div>
        <div>
          <h3>{{ directionP.name }}</h3>
          <p>{{ directionP.description || 'Direction de tête' }}</p>
        </div>
        <div class="mgr">Directeur / Directrice<b>{{ directionP.pole_manager_name || directionP.manager_name || '—' }}</b></div>
      </div>

      <!-- GROUPES / PÔLES -->
      <div class="dgroup" v-for="group in groups" :key="group.pole">
        <div class="gh">
          <span class="chip">{{ group.pole }}</span>
          <h3>{{ group.mgr }}</h3>
        </div>
        <div class="dcards">
          <div
            v-for="d in group.items"
            :key="d.id"
            class="dcard clickable"
            :class="{ mine: isMyDirection(d) }"
            @click="openDirection(d.id)"
          >
            <span v-if="isMyDirection(d)" class="tagme">MOI</span>
            <div class="ic">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/></svg>
            </div>
            <h4>{{ d.name }}</h4>
            <div class="mgr">
              <span class="av">{{ initials(d.manager_name) }}</span>{{ d.manager_name || '—' }}
            </div>
            <div class="foot">
              <span class="open">
                Ouvrir
                <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && directions.length === 0" style="text-align:center;padding:40px">
        Aucune direction trouvée.
      </div>
    </template>
  </div>
</template>
