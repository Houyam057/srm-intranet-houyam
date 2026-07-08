<script setup>
import { ref } from 'vue'

const moods = [
  { value: 4, emoji: '😄', label: 'Très satisfait' },
  { value: 3, emoji: '🙂', label: 'Satisfait' },
  { value: 2, emoji: '😐', label: 'Neutre' },
  { value: 1, emoji: '🙁', label: 'Insatisfait' }
]

const results = [
  { emoji: '😄', pct: 46, color: 'var(--green)' },
  { emoji: '🙂', pct: 36, color: '#7cc98f' },
  { emoji: '😐', pct: 12, color: '#f4b400' },
  { emoji: '🙁', pct: 6, color: 'var(--red)' }
]

const selected = ref(null)

function selectMood(value) {
  selected.value = value
  // Ici : POST /api/mood { value } vers l'API Express
}
</script>

<template>
  <div class="card card-pad">
    <div class="card-h"><h3>Satisfaction de nos collaborateurs</h3></div>
    <p style="font-size:12.5px;color:var(--muted)">Comment vous sentez-vous au travail aujourd'hui ? Votre réponse est anonyme.</p>

    <div class="mood-row">
      <div
        v-for="m in moods"
        :key="m.value"
        class="mood"
        :class="{ sel: selected === m.value }"
        @click="selectMood(m.value)"
      >
        <span class="em">{{ m.emoji }}</span><span>{{ m.label }}</span>
      </div>
    </div>

    <div class="mood-thanks" :class="{ show: selected !== null }">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
      Merci ! Votre humeur du jour a bien été enregistrée.
    </div>

    <div class="mood-res">
      <div class="t">Baromètre du mois — Juin 2026 (1 087 réponses)</div>
      <div class="line" v-for="r in results" :key="r.emoji">
        <span class="lb">{{ r.emoji }}</span>
        <div class="bar"><i :style="{ width: r.pct + '%', background: r.color }"></i></div>
        <span class="pc">{{ r.pct }}%</span>
      </div>
    </div>
  </div>
</template>
