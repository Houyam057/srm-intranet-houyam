<script setup>
import { onMounted, ref } from 'vue'
import HeroCarousel from '../components/HeroCarousel.vue'
import MoodBarometer from '../components/MoodBarometer.vue'
import KPI from '../components/KPI.vue'
import { odooApi } from '../api/odoo.js'

// Dans une vraie appli, ces tableaux viendraient d'appels à l'API Express :
// GET /api/kpi, GET /api/notes-service, GET /api/actualites, GET /api/flash-info
const notes = [
  { text: 'Organisation des horaires durant la période estivale', date: '26/06/2026' },
  { text: 'Campagne de sensibilisation à la sécurité électrique', date: '24/06/2026' },
  { text: "Mise à jour de la procédure de gestion des interventions", date: '20/06/2026' }
]

const services = [
  'Demandes de service SI (helpdesk)',
  'Suivi du courrier',
  'Portail RH / Congés',
  'Plateforme analytique (BI)',
  'Accès applicatifs (Wat.erp · SAP)'
]

const pratique = [
  'Annuaire / Rép. téléphonique',
  'Photothèque',
  'Charte informatique',
  'Publications & guides',
  'Liens utiles'
]

const articles = ref([
  { cat: 'ENTREPRISE', catClass: 'cat-ent', date: '18 Juin 2026', title: 'Signature de la convention de partenariat avec les communes' },
  { cat: 'RÉGIONS', catClass: 'cat-reg', date: '14 Juin 2026', title: "Mise en service d'une nouvelle station d'épuration (STEP)" },
  { cat: 'QSE', catClass: 'cat-qse', date: '11 Juin 2026', title: 'Certification ISO 45001 : la SST récompensée' }
])

const flash = {
  tag: 'FLASH INFO',
  important: true,
  title: 'Maintenance planifiée du réseau — dimanche 12 juillet',
  text: "Une coupure d'eau potable est prévue de 22h à 5h sur le secteur nord pour travaux."
}

onMounted(async () => {
  try {
    const response = await odooApi.get('/api/news')
    const news = response.data?.data?.news || []
    if (news.length) {
      articles.value = news.map((item) => ({
        cat: item.category || 'ACTUALITÉ',
        catClass: 'cat-ent',
        date: item.published_date ? new Date(item.published_date).toLocaleDateString('fr-FR') : '',
        title: item.title
      }))
    }
  } catch {
    // Keep local mock data when Odoo is not reachable.
  }
})
</script>

<template>
  <div class="page page-accueil show">
    <!-- FLASH INFO -->
    <div class="card flash" style="margin-bottom:20px">
      <div class="tag">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/></svg>
        {{ flash.tag }}
      </div>
      <span v-if="flash.important" class="imp">IMPORTANT</span>
      <div class="txt">
        <b>{{ flash.title }}</b>
        <p>{{ flash.text }}</p>
      </div>
      <div class="more">En savoir plus
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </div>
    </div>

    <!-- BANNIÈRE / CARROUSEL -->
    <HeroCarousel />

    <!-- KPI -->
     <div class="card card-pad" style="margin-top:20px">
      <KPI /> 
     </div>
    <!-- ARTICLES + SUGGESTIONS + MOOD -->
    <div class="grid" style="grid-template-columns:1.6fr 1fr;margin-top:20px">
      <div class="card card-pad art-main">
        <div class="card-h"><h3>Actualités</h3><span class="see">Voir tout</span></div>
        <div class="art-hero"></div>
        <div class="art-lead">
          <span class="art-tag">ENTREPRISE</span><span class="art-date">18 Juin 2026</span>
          <h4>Signature de la convention de partenariat avec les communes</h4>
          <p>La SRM-TTA renforce sa collaboration avec les collectivités locales pour améliorer la qualité de service.</p>
        </div>
        <div class="art-list" style="margin-top:16px">
          <div class="art-item" v-for="(a, i) in articles" :key="i">
            <div class="th"></div>
            <div>
              <div class="date"><span class="ncat" :class="a.catClass">{{ a.cat }}</span>{{ a.date }}</div>
              <h5>{{ a.title }}</h5>
            </div>
          </div>
        </div>
        <div class="btn-ghost" style="border-style:solid;margin-top:16px">Voir toutes les actualités
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:20px">
        <div class="card card-pad">
          <div class="card-h"><h3>Boîte à suggestions</h3></div>
          <div class="sugg">
            <div class="bulb">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>
            </div>
            <b>Votre avis compte !</b>
            <p>Partagez vos idées et suggestions pour améliorer notre environnement de travail.</p>
            <button class="btn-primary">Soumettre une suggestion</button>
          </div>
        </div>

        <MoodBarometer />
      </div>
    </div>

    <!-- NOTES + SERVICES + PRATIQUE -->
    <div class="grid" style="grid-template-columns:1.25fr 1fr 1fr;margin-top:20px">
      <div class="card card-pad">
        <div class="card-h"><h3>Notes de service</h3><span class="see">Voir tout</span></div>
        <div class="note" v-for="(n, i) in notes" :key="i">
          <div class="ic">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>
          </div>
          <div class="b"><p>{{ n.text }}</p></div>
          <div class="date">{{ n.date }}</div>
        </div>
        <div class="btn-ghost">Accéder à toutes les notes
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Services</h3></div>
        <div class="svc">
          <a v-for="(s, i) in services" :key="i">
            <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg></span>{{ s }}
          </a>
        </div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Pratique</h3></div>
        <div class="svc">
          <a v-for="(p, i) in pratique" :key="i">
            <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/></svg></span>{{ p }}
          </a>
        </div>
      </div>
    </div>

    <!-- DIGITAL LEARNING -->
    <div class="dlearn">
      <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/></svg></div>
      <div><b>Digital Learning — se former en ligne</b><span>Catalogue de formations, parcours métiers et habilitations obligatoires</span></div>
      <span class="go"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
    </div>
  </div>
</template>
