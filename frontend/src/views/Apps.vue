
<script setup>
import { useRouter } from "vue-router"
import SAPBI from "../assets/sap-bi.svg"
import SAP from "../assets/sap.svg"
import SOMEI from "../assets/somei.svg"
const router = useRouter()
const apps = [
  {
    id: 1,
    name: "Odoo",
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/odoo.svg",
    description: "Une plateforme de gestion intégrée permettant de centraliser les processus métiers de notre organisation",
    url:"https://eservices.srm-tta.ma/odoo?db=SRM_TTA_PROD"
  },
  {
    id: 2,
    name: "SAP",
    icon: SAP,
    description: "Gérez les processus clés de l'entreprise grâce à SAP : finance, achats, ventes, logistique et gestion des ressources.",
  },
  {
    id: 3,
    name: "SAP BI",
    icon: SAPBI,
    description: "Plateforme d'analyse décisionnelle offrant des rapports, tableaux de bord et indicateurs de performance en temps réel.",
    url: "http://s09pp-bob-rpt01.srm-tth.local:8080/BOE/BI"
  },
  {
    id: 4,
    name: "WatErp / Somei",
    icon: SOMEI,
    description: "Wat.erp simplifie la gestion de l'eau et de l'assainissement : abonnements, télérelevé, détection de fuites, facturation et espace client.",
    url: "https://identity-tth.srm-tth.local/login?signin=2552753e197809c75cebf12a825d1ab7"
  }
]

const openApp = (url) => {
  if(!url) {return;}
  window.open(url, "_blank"); 
};
</script>

<template>
   <div class="page page-direction show">
    <div class="crumbs">
            Accueil <span class="sep">›</span>
            <span class="cur">Outils & Applications</span>
    </div>
    <div class="card-h">
         <h3>Nos Applications</h3>
    </div>

    <div class="apps-grid">
      <div
        class="app-card"
        v-for="app in apps"
        :key="app.id"
      >
        <div class="icon">
          <img :src="app.icon" :alt="app.name" />
        </div>

        <h2>{{ app.name }}</h2>

        <p>
          {{ app.description }}
        </p>

        <div class="actions">
            <button @click="openApp(app.url)">
                Open
            </button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.header {
  text-align: center;
  margin-bottom: 50px;
}

.header h1 {
  font-size: 42px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.header p {
  color: #6c757d;
  font-size: 18px;
}

.apps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.app-card {
  display:flex;
  background: white;
  border : 1px solid transparent;
  border-radius: 18px;
  padding: 35px;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0,0,0,.08);
  transition: .3s;
  margin-top:25px;
  flex-direction: column;

}

.app-card:hover {
  transform: scale(1.015);
  box-shadow: 0 15px 40px rgba(0,0,0,.12);
  border: 1px solid var(--navy)
}

.icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.icon img {
  width: 120px;
  height: 120px;
  object-fit: contain;
}

.app-card h2 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.app-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
}

.actions {
    margin-top: auto;
}

button {
  background: var(--navy);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  transition: .2s;
  margin-top:auto;
}

button:hover {
  background: #0a2454
  
}
</style>