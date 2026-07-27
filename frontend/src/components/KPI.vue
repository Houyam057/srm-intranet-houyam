<script setup>
import { ref, onMounted } from 'vue'
import { ChartNoAxesCombined } from 'lucide-vue-next'
import { odooApi } from '../api/odoo.js'

const props = defineProps({
  directionId: { type: [Number, String], default: null }
})

const kpis = ref([])
const loading = ref(true)

const COLORS = ['navy', 'muted', 'red', 'green']

onMounted(async () => {
  try {
    const params = {}
    if (props.directionId) {
      params.direction_id = props.directionId
    }
    const response = await odooApi.get('/api/kpis', { params })
    const data = response.data?.data?.kpis || []
    if (data.length) {
      kpis.value = data.map((k) => ({
        ...k,
        val: k.val ? `${k.val}` : '—',
      }))
    } 
  } catch (e) {
    console.error('Erreur chargement KPIs:', e.response?.status, e.response?.data || e.message)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="kpi-row">
    <div v-if="loading" class="kpi" v-for="n in 4" :key="n">
      <div class="skeleton" style="height:20px;width:60%;margin-bottom:8px"></div>
      <div class="skeleton" style="height:32px;width:40%;margin-bottom:8px"></div>
      <div class="skeleton" style="height:14px;width:80%"></div>
    </div>
    <template v-else>
      <div class="kpi" v-for="(k, i) in kpis" :key="i">
        <div class="head">
          <div class="ic" :class="'ic-' + COLORS[i % COLORS.length]">
            <ChartNoAxesCombined :size="24" />
          </div>
          <h2>{{ k.name }}</h2>
        </div>
        <div class="val">{{ k.val }} %</div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.skeleton {
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
