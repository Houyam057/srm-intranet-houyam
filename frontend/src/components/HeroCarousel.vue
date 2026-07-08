<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const slides = [
  {
    eyebrow: 'Portail interne · SRM-TTA',
    title: 'BIENVENUE',
    sub: "L'intranet qui rapproche toutes nos directions, nos métiers et nos collaborateurs.",
    gradient: 'linear-gradient(100deg,#0b2a66 0%,#123a8a 48%,rgba(18,58,138,.55) 66%,rgba(18,58,138,0) 85%)'
  },
  {
    eyebrow: 'Actualité entreprise',
    title: 'ENGAGEMENT',
    sub: 'Nos équipes sur le terrain, chaque jour, au service de nos clients et de nos territoires.',
    gradient: 'linear-gradient(100deg,#0d2a63 0%,#1a4aa0 48%,rgba(26,74,160,.5) 68%,rgba(26,74,160,0) 88%)'
  },
  {
    eyebrow: 'Qualité & Sécurité',
    title: 'EXCELLENCE',
    sub: 'La sécurité de tous, notre priorité au quotidien — certifiée ISO 45001.',
    gradient: 'linear-gradient(100deg,#123a8a 0%,#1f5fd6 48%,rgba(31,95,214,.5) 68%,rgba(31,95,214,0) 88%)'
  }
]

const current = ref(0)
let timer = null

function show(i) {
  current.value = (i + slides.length) % slides.length
}

onMounted(() => {
  timer = setInterval(() => show(current.value + 1), 7000)
})
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="hero hero-accueil" style="min-height:270px">
    <div
      v-for="(s, i) in slides"
      :key="i"
      class="hslide"
      :class="{ on: i === current }"
    >
      <div class="bg" :style="{ background: s.gradient }"></div>
      <div class="hero-photo" style="width:56%">
        <div class="sky-scene">
          <div class="sun"></div>
        </div>
      </div>
      <div class="content">
        <div class="eyebrow">{{ s.eyebrow }}</div>
        <h1>{{ s.title }}</h1>
        <div class="tri-hero"></div>
        <p class="sub">{{ s.sub }}</p>
      </div>
    </div>

    <div class="hdots">
      <i v-for="(s, i) in slides" :key="i" :class="{ on: i === current }" @click="show(i)"></i>
    </div>
  </div>
</template>
