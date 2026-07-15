<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { Pencil, X, Save, LogOut } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('profile')

const editing = reactive({
  personal: false,
  professional: false
})

const backup = reactive({
  personal: {},
  professional: {}
})

const user = reactive({
  name: '',
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  company: '',
  jobTitle: '',
  website: ''
})

const personalFields = ['firstName', 'lastName', 'email', 'phone']
const professionalFields = ['company', 'jobTitle', 'website']

onMounted(() => {
  user.name = authStore.user?.name || 'Claire Someone'
  user.email = authStore.user?.email || 'Claire.someone@test.com'
  user.firstName = authStore.user?.firstName || 'Claire'
  user.lastName = authStore.user?.lastName || 'Someone'
  user.phone = authStore.user?.phone || '+1 (781) 588-5959'
  user.company = authStore.user?.company || "Kyle's designs"
  user.jobTitle = authStore.user?.jobTitle || 'Durations analyst'
  user.website = authStore.user?.website || 'https://kylesportfolio.framer.website/'
})

function toggleEdit(section) {
  if (!editing[section]) {
    const fields = section === 'personal' ? personalFields : professionalFields
    backup[section] = fields.reduce((acc, f) => ({ ...acc, [f]: user[f] }), {})
  } else {
    const fields = section === 'personal' ? personalFields : professionalFields
    fields.forEach(f => { user[f] = backup[section][f] })
  }
  editing[section] = !editing[section]
}

function save(section) {
  editing[section] = false
}

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}

</script>

<template>
  <div class="page show">
    <div class="crumbs">
      Accueil <span class="sep">›</span>
      <span class="cur">Mon Profil</span>
    </div>
      <!-- Main Content -->
      <main>
        <!-- Profile Tab -->
          <div class="card card-pad" style="margin-bottom:20px">
            <div class="card-h">
              <h3>Informations du profil</h3>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
                <div style="grid-column:span 2;display:flex;align-items:center;gap:20px;margin-bottom:16px">
              <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#2b5cad,#0f2f6b);color:#fff;display:grid;place-items:center;font-weight:700;font-size:24px;flex:none">
                {{ user.firstName?.[0] }}{{ user.lastName?.[0] }}
              </div>
              <h2 style="font-size:18px;font-weight:800">{{ user.firstName }} {{ user.lastName }}</h2>
            </div>
            <!--<div class="card-h">
              <div style="display:flex;gap:8px;margin-left:auto">
                <button :class="['btn-primary', editing.personal ? 'btn-cancel' : '']" style="padding:8px 16px;font-size:12px" @click="toggleEdit('personal')">
                  <Pencil v-if="!editing.personal" :size="14" />
                  <X v-else :size="14" />
                  {{ editing.personal ? 'Annuler' : 'Modifier' }}
                </button>
                <button v-if="editing.personal" class="btn-primary btn-save" style="padding:8px 16px;font-size:12px" @click="save('personal')">
                  <Save :size="14" />
                  Sauvegarder
                </button>
              </div>
            </div>
        -->

              <div class="form-group">
                <label class="floating-label">
                  <span>Email</span>
                  <input v-model="user.email" type="email" :readonly="!editing.personal" />
                </label>
              </div>
              <div class="form-group">
                <label class="floating-label">
                  <span>Téléphone</span>
                  <input v-model="user.phone" type="tel" :readonly="!editing.personal" />
                </label>
              </div>
            </div>
            <div style="display:flex;justify-content:flex-end;margin-top:16px">
              <button class="btn-primary btn-logout" style="flex:none;white-space:nowrap" @click="handleLogout">
                <LogOut :size="14" />
                Se déconnecter
              </button>
            </div>
          </div>

          <!-- Professional Information -->
          <div class="card card-pad">
            <div class="card-h">
              <h3>Informations professionnelles</h3>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
              <div class="form-group">
                <label class="floating-label">
                  <span>Direction</span>
                  <div class="text-static" style="width:100%">{{ user.company }}</div>
                </label>
              </div>
              <div class="form-group">
                <label class="floating-label">
                  <span>Role</span>
                  <div class="text-static" style="width:100%">{{ user.jobTitle }}</div>
                </label>
              </div>
            </div>
          </div>
        <!-- Other Tabs -->
      </main>
    </div>
</template>

<style scoped>
.btn-cancel {
  background: var(--red) !important;
}
.btn-cancel:hover {
  background: #b71c1c !important;
}
.btn-save {
  background: var(--green) !important;
}
.btn-save:hover {
  background: var(--green-2) !important;
}
.btn-logout {
  background: var(--red) !important;
}
.btn-logout:hover {
  background: white !important;
  color: var(--red) !important;
  border : 1px solid var(--red) !important;
}
</style>