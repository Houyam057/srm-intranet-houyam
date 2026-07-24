<script setup>
import { ref, onMounted } from 'vue'
import { odooApi } from '../api/odoo.js'

const documents = ref([])
const loading = ref(true)
const error = ref(false)

const FT_CLASS = { pdf: 'ft-pdf', docx: 'ft-doc', pptx: 'ft-ppt' }
function ftClass(type) {
  return FT_CLASS[type] || 'ft-zip'
}
function ftLabel(type) {
  return (type || 'other').toUpperCase()
}
function downloadUrl(doc) {
  return `/api/documents/${doc.id}/download`
}

onMounted(async () => {
  try {
    const response = await odooApi.get('/api/documents')
    documents.value = response.data?.data?.documents || []
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page page-documents show">
    <div class="crumbs">
      Accueil <span class="sep">›</span>
      <span class="cur">Documents &amp; Procédures</span>
    </div>

    <div class="gd-hero">
      <div class="kicker">Ressources</div>
      <h1>Documents &amp; Procédures</h1>
      <div class="tri-h"></div>
    </div>

    <div class="card card-pad" style="margin-top:20px">
      <div class="card-h"><h3>Documents disponibles</h3></div>

      <div v-if="loading" style="color:var(--muted);font-size:13px">Chargement...</div>
      <div v-else-if="error" style="color:var(--muted);font-size:13px">
        Impossible de charger les documents pour le moment.
      </div>
      <div v-else-if="documents.length === 0" style="color:var(--muted);font-size:13px">
        Aucun document disponible pour le moment.
      </div>
      <div v-else class="grid" style="gap:12px">
        <a
          v-for="d in documents"
          :key="d.id"
          class="doc"
          :href="downloadUrl(d)"
          style="text-decoration:none;color:inherit"
        >
          <div class="ft" :class="ftClass(d.file_type)">{{ ftLabel(d.file_type) }}</div>
          <div class="b">
            <b>{{ d.name }}</b>
            <span>{{ d.category }} · {{ d.file_size }}</span>
          </div>
          <div class="dl">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>
