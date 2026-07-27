<script setup>
import { ref, computed, onMounted } from 'vue'
import { odooApi } from '../api/odoo.js'
import {ClockFading} from 'lucide-vue-next'

const moods = [
  { value: 'very_good', emoji: '😄', label: 'Très satisfait' },
  { value: 'good', emoji: '🙂', label: 'Satisfait' },
  { value: 'neutral', emoji: '😐', label: 'Neutre' },
  { value: 'bad', emoji: '🙁', label: 'Insatisfait' }
]

const moodOrder = ['very_good', 'good', 'neutral', 'bad']

const stats = ref({ very_good: 0, good: 0, neutral: 0, bad: 0 })
const totalVotes = computed(() => Object.values(stats.value).reduce((a, b) => a + b, 0))
const results = computed(() =>
  moodOrder.map((key, i) => {
    const pct = totalVotes.value ? Math.round((stats.value[key] / totalVotes.value) * 100) : 0
    return { emoji: moods[i].emoji, pct, color: ['var(--green)', '#7cc98f', '#f4b400', 'var(--red)'][i] }
  })
)

const selected = ref(null)
const canVote = ref(true)
const cooldownText = ref('')
const submitting = ref(false)
const errorMsg = ref('')

let cooldownInterval = null
let remainingSeconds = 0

function updateCooldownText() {
  if (remainingSeconds <= 0) {
    canVote.value = true
    cooldownText.value = ''
    clearInterval(cooldownInterval)
    return
  }
  remainingSeconds--
  const h = Math.floor(remainingSeconds / 3600)
  const m = Math.floor((remainingSeconds % 3600) / 60)
  const s = remainingSeconds % 60
  cooldownText.value = `${h}h ${String(m).padStart(2, '0')}min ${String(s).padStart(2, '0')}s`
}

function startCooldown(seconds) {
  remainingSeconds = seconds
  updateCooldownText()
  if (cooldownInterval) clearInterval(cooldownInterval)
  cooldownInterval = setInterval(updateCooldownText, 1000)
}

onMounted(async () => {
  try {
    const res = await odooApi.get('/api/feedback/status')
    const data = res.data?.data
    if (data) {
      stats.value = data.stats || {}
      canVote.value = data.can_vote !== false
      if (!canVote.value && data.remaining_seconds > 0) {
        startCooldown(data.remaining_seconds)
      }
    }
  } catch {
    // fallback: allow voting
  }
})

async function selectMood(moodValue) {
  if (!canVote.value || submitting.value) return
  errorMsg.value = ''
  selected.value = moodValue
  submitting.value = true
  try {
    await odooApi.post('/api/feedback', { mood: moodValue })
    const res = await odooApi.get('/api/feedback/status')
    const data = res.data?.data
    if (data) {
      stats.value = data.stats || {}
      canVote.value = data.can_vote !== false
      if (!canVote.value && data.remaining_seconds > 0) {
        startCooldown(data.remaining_seconds)
      }
    }
  } catch (e) {
    selected.value = null
    errorMsg.value = e.response?.data?.error || 'Erreur lors de l\'envoi.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="card card-pad">
    <div class="card-h"><h3>Satisfaction de nos collaborateurs</h3></div>

    <template v-if="canVote">
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
    </template>

    <div v-else class="cooldown-msg">
      <span class="cooldown-icon"><ClockFading /></span>
      <div>
        <b>Vous avez déjà voté.</b>
        <p>Prochain vote dans : <span class="cooldown-timer">{{ cooldownText }}</span></p>
      </div>
    </div>

    <p v-if="errorMsg" style="font-size:12px;color:var(--red);margin:8px 0 0">{{ errorMsg }}</p>

    <div class="mood-thanks" :class="{ show: selected !== null && canVote }">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
      Merci ! Votre humeur du jour a bien été enregistrée.
    </div>

    <div class="mood-res">
      <div class="t">Baromètre — {{ totalVotes }} réponses</div>
      <div class="line" v-for="r in results" :key="r.emoji">
        <span class="lb">{{ r.emoji }}</span>
        <div class="bar"><i :style="{ width: r.pct + '%', background: r.color }"></i></div>
        <span class="pc">{{ r.pct }}%</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cooldown-msg {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 10px;
  margin: 8px 0;
}
.cooldown-icon {
  font-size: 28px;
}
.cooldown-msg b {
  font-size: 13px;
  color: var(--ink, #1a1a2e);
  display: block;
  margin-bottom: 2px;
}
.cooldown-msg p {
  margin: 0;
  font-size: 12px;
  color: var(--muted, #888);
}
.cooldown-timer {
  font-weight: 700;
  color: var(--navy, #0f2f6b);
}
</style>
