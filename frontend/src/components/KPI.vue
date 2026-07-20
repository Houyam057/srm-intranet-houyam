 <script setup >
 import { Users,MessageSquareMore,DollarSign } from 'lucide-vue-next';
 
const kpis = [
  { icon: Users, color: 'navy', label: "Clients satisfaits", val: '87%', trend: '+3 pts vs mois dernier', tag: 'CLIENTÈLE' },
  { icon: DollarSign, color: 'green', label: 'Taux de recouvrement', val: '99.2%', trend: '+0.4 pt vs mois dernier', tag: 'EXPLOITATIONS' },
  { icon: MessageSquareMore, color: 'red', label: "Réclamations traitées", val: '96%', trend: '+5 pts vs mois dernier', tag: 'DSI' },
  { icon: MessageSquareMore, color: 'red', label: "Réclamations traitées", val: '96%', trend: '+5 pts vs mois dernier', tag: 'DSI' }

]
</script>
 <template>
 <!-- KPI -->
    <div class="grid" style="margin-top:20px">
      <div class="card-h" style="margin-bottom:0"><h3>Indicateurs clés</h3></div>
      <div class="kpi-row">
        <div class="kpi" v-for="(k, i) in kpis" :key="i">
          <div class="head">
            <div class="ic" :class="'ic-' + k.color">
              <component :is="k.icon" :size="24" />
            </div>
            <h2>{{ k.label }}</h2>
            <span class="dirtag">{{ k.tag }}</span>
          </div>
          <div class="val">{{ k.val }}</div>
          <div class="trend">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M17 7H8M17 7v9"/></svg>
            {{ k.trend }}
          </div>
        </div>
      </div>
    </div>
</template>