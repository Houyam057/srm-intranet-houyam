<script setup>
import { ref, reactive } from 'vue'
import { odooApi } from '../api/odoo.js'
import { X } from 'lucide-vue-next'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close', 'submitted'])

const form = reactive({
  title: '',
  category: 'amelioration',
  message: ''
})

const submitting = ref(false)
const error = ref('')

const categories = [
  { value: 'amelioration', label: 'Amélioration' },
  { value: 'innovation', label: 'Innovation' },
  { value: 'environnement', label: 'Environnement de travail' },
  { value: 'processus', label: 'Processus' },
  { value: 'autre', label: 'Autre' }
]

async function submit() {
  error.value = ''
  if (!form.title.trim() || !form.message.trim()) {
    error.value = 'Veuillez remplir tous les champs.'
    return
  }
  submitting.value = true
  try {
    await odooApi.post('/api/suggestions', {
      title: form.title,
      category: form.category,
      message: form.message
    })
    form.title = ''
    form.category = 'amelioration'
    form.message = ''
    emit('submitted')
    emit('close')
  } catch (e) {
    error.value = e.response?.data?.error || 'Erreur lors de la soumission.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-box">
        <div class="modal-header">
          <h3>Soumettre une suggestion</h3>
          <button class="modal-close" @click="$emit('close')"><X :size="18" /></button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Titre</label>
            <input v-model="form.title" type="text" placeholder="Titre de votre suggestion" />
          </div>
          <div class="form-group">
            <label>Catégorie</label>
            <select v-model="form.category">
              <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.message" rows="5" placeholder="Décrivez votre suggestion..."></textarea>
          </div>
          <p v-if="error" class="error-msg">{{ error }}</p>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="$emit('close')">Annuler</button>
          <button class="btn-submit" @click="submit" :disabled="submitting">
            {{ submitting ? 'Envoi...' : 'Soumettre' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
  z-index: 9999;
}
.modal-box {
  background: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--line, #e5e7eb);
}
.modal-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--navy, #0f2f6b);
}
.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--muted, #888);
  padding: 4px;
  border-radius: 6px;
}
.modal-close:hover {
  background: var(--blue-soft, #f0f4ff);
  color: var(--navy, #0f2f6b);
}
.modal-body {
  padding: 20px;
}
.form-group {
  margin-bottom: 14px;
}
.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink, #1a1a2e);
  margin-bottom: 6px;
}
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--line, #e5e7eb);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  color: var(--ink, #1a1a2e);
  background: #fff;
  box-sizing: border-box;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--navy, #0f2f6b);
  box-shadow: 0 0 0 3px rgba(15, 47, 107, 0.1);
}
.form-group textarea {
  resize: vertical;
}
.error-msg {
  color: var(--red, #dc3545);
  font-size: 13px;
  margin: 0;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid var(--line, #e5e7eb);
}
.btn-cancel {
  padding: 8px 16px;
  border: 1px solid var(--line, #e5e7eb);
  border-radius: 8px;
  background: #fff;
  color: var(--ink, #1a1a2e);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}
.btn-cancel:hover {
  background: var(--blue-soft, #f0f4ff);
}
.btn-submit {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: var(--navy, #0f2f6b);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}
.btn-submit:hover {
  background: var(--blue, #2b5cad);
}
.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
