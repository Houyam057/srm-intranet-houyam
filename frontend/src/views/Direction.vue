<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// Dans une vraie appli : GET /api/directions/comm/dashboard
const quickLinks = [
  'Plan de communication', 'Charte graphique SRM-TTA', 'Demande de publication',
  'Supports & Templates', 'Médiathèque', 'Suivi des campagnes'
]

const actus = [
  { date: '26 Juin 2026', title: 'Nouvelle campagne SMS Info', text: 'Lancement de la campagne de sensibilisation sur les nouveaux canaux de paiement.', grad: 'linear-gradient(135deg,#c0392b,#7a1f16)' },
  { date: '23 Juin 2026', title: 'SRM-TTA lance son nouveau site web', text: "Découvrez le nouveau site institutionnel conçu pour une meilleure expérience utilisateur.", grad: 'linear-gradient(135deg,#2f8fc0,#1c5675)' },
  { date: '18 Juin 2026', title: 'Retour sur notre participation au Salon Service Public 2026', text: 'Un stand, des échanges et de belles rencontres.', grad: 'linear-gradient(135deg,#3a5f8a,#22364f)' }
]

const projets = [
  { title: 'Refonte site web SRM-TTA', sub: 'Phase de développement', pct: 75 },
  { title: 'Campagne digital – Été 2026', sub: 'Création des visuels', pct: 60 },
  { title: 'Rebranding réseaux sociaux', sub: 'Déploiement en cours', pct: 45 }
]

const notes = [
  { text: 'Organisation des horaires durant la période estivale', date: '26/06/2026' },
  { text: 'Campagne de sensibilisation à la sécurité électrique', date: '24/06/2026' },
  { text: 'Mise à jour de la procédure de gestion des interventions', date: '20/06/2026' },
  { text: 'Rappel – Utilisation de la charte graphique', date: '18/06/2026' }
]

const docs = [
  { name: 'Charte graphique SRM-TTA', meta: 'PDF · 3.2 Mo', type: 'pdf' },
  { name: 'Présentation institutionnelle', meta: 'PPTX · 8.7 Mo', type: 'ppt' },
  { name: 'Guide réseaux sociaux', meta: 'PDF · 2.1 Mo', type: 'pdf' },
  { name: 'Modèles de publications', meta: 'ZIP · 12.4 Mo', type: 'zip' }
]

const calendrier = [
  { d: 'LUN', date: '23 JUIN', color: 'c-fb', label: 'Post Facebook', sub: 'Conseils sécurité' },
  { d: 'MAR', date: '24 JUIN', color: 'c-ig', label: 'Story Instagram', sub: 'Info service' },
  { d: 'MER', date: '25 JUIN', color: 'c-in', label: 'Post LinkedIn', sub: 'Actualité entreprise' },
  { d: 'JEU', date: '26 JUIN', color: 'c-yt', label: 'Vidéo YouTube', sub: 'Présentation projet' },
  { d: 'VEN', date: '27 JUIN', color: 'c-fb', label: 'Post Facebook', sub: 'Éco-gestes' }
]

const metrics = [
  { icon: 'navy', val: '42', lbl: 'Publications réalisées ce mois-ci', trend: '+12% vs Mai 2026' },
  { icon: 'green', val: '28 450', lbl: 'Abonnés cumulés sur nos réseaux', trend: '+8% vs Mai 2026' },
  { icon: 'navy', val: '512 300', lbl: 'Impressions ce mois-ci', trend: '+14% vs Mai 2026' },
  { icon: 'red', val: '24 680', lbl: 'Engagements totaux', trend: '+16% vs Mai 2026' },
  { icon: 'navy', val: '1 248', lbl: 'Téléchargements documents', trend: '+10% vs Mai 2026' }
]
</script>

<template>
  <div class="page page-direction show">
    <div class="crumbs">  
      Accueil <span class="sep">›</span>
      <span class="lnk" @click="router.push({ name: 'mesdirections' })">Nos Directions</span>
      <span class="sep">›</span>
      <span class="cur">Communication &amp; Marketing</span>
    </div>

    <!-- HERO DIRECTION -->
    <div class="hero hero-dir">
      <div class="bg"></div>
      <div class="hero-photo hero-photo-dir"></div>
      <div class="badge-ic">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l14-6v14l-14-6z"/><path d="M17 8a4 4 0 0 1 0 6M7 11v5a2 2 0 0 0 2 2"/></svg>
      </div>
      <div class="content">
        <div class="kicker">Direction</div>
        <h1>Communication &amp; Marketing</h1>
        <div class="tri-hero"></div>
        <p class="sub"><b>Informer, valoriser, engager.</b><br>Nous pilotons la communication interne et externe de la SRM-TTA et renforçons l'image et la notoriété de l'entreprise.</p>
        <div class="pills">
          <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>Transparence</div>
          <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>Créativité</div>
          <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg>Engagement</div>
          <div><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/></svg>Impact</div>
        </div>
      </div>
    </div>

    <!-- ROW 1: 4 colonnes -->
    <div class="grid" style="grid-template-columns:repeat(4,1fr);margin-top:20px">
      <div class="card card-pad">
        <div class="card-h"><h3>Accès rapides</h3></div>
        <div class="qa-grid" style="grid-template-columns:repeat(3,1fr);gap:10px">
          <div class="qa" style="padding:14px 4px" v-for="(l, i) in quickLinks" :key="i">
            <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div>
            <span>{{ l }}</span>
          </div>
        </div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Actualités de la direction</h3><span class="see">Voir tout</span></div>
        <div class="dir-actu" v-for="(a, i) in actus" :key="i">
          <div class="th" :style="{ background: a.grad }"></div>
          <div>
            <div class="date">{{ a.date }}</div>
            <h4>{{ a.title }}</h4>
            <p>{{ a.text }}</p>
          </div>
        </div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Projets en cours</h3><span class="see">Voir tout</span></div>
        <div class="proj" v-for="(p, i) in projets" :key="i">
          <div class="top">
            <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg></div>
            <div style="flex:1"><h4>{{ p.title }}</h4><div class="sub">{{ p.sub }}</div></div>
          </div>
          <div class="bar"><i :style="{ width: p.pct + '%' }"></i></div><div class="pct">{{ p.pct }}%</div>
        </div>
        <div class="btn-ghost" style="border-style:solid">Tous les projets <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
      </div>

      <div class="card card-pad">
        <div class="card-h"><h3>Notes de service</h3><span class="see">Voir tout</span></div>
        <div class="note" v-for="(n, i) in notes" :key="i">
          <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg></div>
          <div class="b"><p>{{ n.text }}</p></div>
          <div class="date">{{ n.date }}</div>
        </div>
        <div class="btn-ghost" style="border-style:solid">Accéder à toutes les notes <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
      </div>
    </div>

    <!-- ROW 2: DOCUMENTS + CALENDRIER -->
    <div class="grid" style="grid-template-columns:1fr 1.6fr;margin-top:20px">
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

      <div class="card card-pad">
        <div class="card-h"><h3>Calendrier éditorial</h3><span class="see">Voir le calendrier</span></div>
        <div class="cal">
          <div class="day" v-for="(c, i) in calendrier" :key="i">
            <div class="d"><b>{{ c.d }}</b><span>{{ c.date }}</span></div>
            <div class="ev"><div class="k"><i :class="c.color"></i>{{ c.label }}</div><p>{{ c.sub }}</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ROW 3: METRICS -->
    <div class="card card-pad" style="margin-top:20px;background:#fbfcfe">
      <div class="section-title"><h3>Nos indicateurs clés</h3></div>
      <div class="metrics" style="margin-top:16px">
        <div class="metric" v-for="(m, i) in metrics" :key="i">
          <div class="ic" :class="'ic-' + m.icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l18-5v12L3 14v-3z"/></svg></div>
          <div class="val">{{ m.val }}</div>
          <div class="lbl">{{ m.lbl }}</div>
          <div class="trend"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M17 7H8M17 7v9"/></svg>{{ m.trend }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
