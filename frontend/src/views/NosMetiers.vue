<script setup>
const metiers = [
  {
    title: 'Distribution d\'eau potable',
    text: "Garantir un accès continu à une eau sanitairement conforme, à travers une infrastructure modernisée et un suivi rigoureux de la qualité.",
    icon: 'M12 2s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z',
    color: 'ic-blue'
  },
  {
    title: 'Distribution d\'électricité',
    text: "Assurer la fiabilité et la sécurité du réseau électrique, avec des efforts continus de modernisation et d'extension de l'infrastructure.",
    icon: 'M13 2 3 14h7l-1 8 10-12h-7z',
    color: 'ic-navy'
  },
  {
    title: 'Assainissement liquide',
    text: "Protéger la santé publique et préserver les écosystèmes naturels, en respectant les normes environnementales en vigueur.",
    icon: 'M12 2v6M8 8h8l2 12H6L8 8z',
    color: 'ic-green'
  }
]

const territoire = [
  { icon: 'navy', val: '8', lbl: 'Provinces et préfectures' },
  { icon: 'green', val: '146', lbl: 'Communes desservies' },
  { icon: 'red', val: '~4M', lbl: "Habitants sur le territoire" },
]
</script>

<template>
  <div class="page page-nosmetiers show">
    <div class="crumbs">
      Accueil <span class="sep">›</span>
      <span class="cur">Nos métiers</span>
    </div>

    <div class="gd-hero">
      <div class="kicker">SRM-TTA</div>
      <h1>Nos métiers</h1>
      <div class="tri-h"></div>
      <p style="max-width:640px;opacity:.95;font-size:14px">
        SRM-TTA gère trois services publics essentiels sur la région
        Tanger-Tétouan-Al Hoceïma, dans le cadre d'un contrat de gestion conclu
        avec le Groupement des Collectivités Territoriales de la région.
      </p>
    </div>

    <div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:20px">
      <div class="card card-pad" v-for="(m, i) in metiers" :key="i">
        <div class="ic" :class="m.color" style="width:52px;height:52px;border-radius:50%;display:grid;place-items:center;margin-bottom:14px">
          <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:24px;height:24px"><path :d="m.icon"/></svg>
        </div>
        <h3 style="font-size:16px;font-weight:800;color:var(--ink);margin-bottom:8px">{{ m.title }}</h3>
        <p style="font-size:13px;color:var(--muted);line-height:1.5">{{ m.text }}</p>
      </div>
    </div>

    <div class="card card-pad" style="margin-top:20px;background:#fbfcfe">
      <div class="section-title"><h3>Notre territoire</h3></div>
      <div class="metrics" style="margin-top:16px">
        <div class="metric" v-for="(t, i) in territoire" :key="i">
          <div class="ic" :class="'ic-' + t.icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l18-5v12L3 14v-3z"/></svg></div>
          <div class="val">{{ t.val }}</div>
          <div class="lbl">{{ t.lbl }}</div>
        </div>
      </div>
    </div>

    <div class="gd-note">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>
      Chiffres et missions issus des sources publiques de SRM-TTA (RADEEL, communiqués officiels) — voir «&nbsp;Notre société&nbsp;» pour le site institutionnel complet.
    </div>
  </div>
</template>
