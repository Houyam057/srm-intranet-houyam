<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { odooApi } from '../api/odoo.js'
import { LogOut, User } from 'lucide-vue-next'
import HorizontalNavBar from '../components/HorizontalNavBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const isAdmin = computed(() => authStore.user?.role === 'admin')

const activeTab = ref('infos')
const tabs = computed(() => {
  const list = [
    { key: 'infos', label: 'Profil' },
    { key: 'emails', label: 'Emails' },
    { key: 'notifications', label: 'Notifications' }
  ]
  if (isAdmin.value) {
    list.splice(1, 0, { key: 'users', label: 'Users' })
  }
  return list
})

const user = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  company: '',
  jobTitle: '',
  role: ''
})

const employees = ref([])
const loadingEmployees = ref(false)
const emails = ref([])
const notifications = ref([])
const loadingEmails = ref(false)

onMounted(async () => {
  await authStore.fetchProfile()
  const u = authStore.user
  const fullName = u?.name || ''
  const parts = fullName.split(' ')
  user.firstName = parts[0] || ''
  user.lastName = parts.slice(1).join(' ') || ''
  user.email = u?.email || ''
  user.phone = u?.phone || ''
  user.company = u?.direction_name || ''
  user.jobTitle = u?.job_title || ''
  user.role = u?.role || ''
})

async function fetchEmployees() {
  loadingEmployees.value = true
  try {
    const res = await odooApi.get('/api/employees')
    employees.value = res.data?.data?.employees || []
  } catch {
    employees.value = []
  } finally {
    loadingEmployees.value = false
  }
}

function onTabChange(key) {
  activeTab.value = key
  if (key === 'users' && employees.value.length === 0) {
    fetchEmployees()
  }
  if (key === 'emails' && emails.value.length === 0) {
    fetchEmails()
  }
  if (key === 'notifications' && notifications.value.length === 0) {
    fetchEmails()
  }
}

async function fetchEmails() {
  loadingEmails.value = true
  try {
    const res = await odooApi.get('/api/emails')
    emails.value = res.data?.data?.emails || []
    notifications.value = res.data?.data?.notifications || []
  } catch {
    emails.value = []
    notifications.value = []
  } finally {
    loadingEmails.value = false
  }
}

async function markAsRead(emailId) {
  try {
    await odooApi.put(`/api/emails/${emailId}/read`)
    const email = emails.value.find(e => e.id === emailId)
    if (email) email.is_read = true
  } catch { /* silent */ }
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

    <HorizontalNavBar :tabs="tabs" :modelValue="activeTab" @update:modelValue="onTabChange" />

    <main style="margin-top: 10px;">
      <!-- Infos Tab -->
      <template v-if="activeTab === 'infos'">
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

            <div class="form-group">
              <label class="floating-label">
                <span>Email</span>
                <input v-model="user.email" type="email" readonly />
              </label>
            </div>
            <div class="form-group">
              <label class="floating-label">
                <span>Téléphone</span>
                <input v-model="user.phone" type="tel" readonly />
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

        <div class="card card-pad">
          <div class="card-h">
            <h3>Informations professionnelles</h3>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">
            <div class="form-group">
              <label class="floating-label">
                <span>Direction</span>
                <div class="text-static" style="width:100%">{{ user.company || '-' }}</div>
              </label>
            </div>
            <div class="form-group">
              <label class="floating-label">
                <span>Poste</span>
                <div class="text-static" style="width:100%">{{ user.jobTitle || '-' }}</div>
              </label>
            </div>
            <div class="form-group">
              <label class="floating-label">
                <span>Role</span>
                <div v-if="user.role==='user'" class="text-static" style="width:100%" >
                    Employée
                </div>
                <div v-if="user.role==='admin'" class="text-static" style="width:100%" >
                    Directeur
                </div>
              </label>
            </div>
          </div>
        </div>
      </template>

      <!-- Users Tab -->
      <template v-if="activeTab === 'users'">
        <div class="card card-pad">
          <div class="card-h">
            <h3>Utilisateurs</h3>
          </div>

          <div v-if="loadingEmployees" style="text-align:center;padding:40px;color:var(--muted)">
            Chargement...
          </div>

          <div v-else-if="employees.length === 0" style="text-align:center;padding:40px;color:var(--muted)">
            Aucun utilisateur trouvé
          </div>

          <div v-else class="table-wrap">
            <table class="users-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nom</th>
                  <th>Email</th>
                  <th>Téléphone</th>
                  <th>Login</th>
                  <th>Rôle</th>
                  <th>Direction</th>
                  <th>Poste</th>
                  <th>Manager</th>
                  <th>Actif</th>
                  <th>Créé le</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="emp in employees" :key="emp.id">
                  <td>{{ emp.id }}</td>
                  <td><b>{{ emp.name }}</b></td>
                  <td>{{ emp.email }}</td>
                  <td>{{ emp.phone || '-' }}</td>
                  <td>{{ emp.login }}</td>
                  <td><span v-if="emp.role" :class="['role-badge', emp.role]">
                    <div v-if="emp.role==='user'">Employé</div>
                    <div v-if="emp.role==='admin'">Directeur</div>
                  </span><span v-else>-</span></td>
                  <td>{{ emp.direction_name || '-' }}</td>
                  <td>{{ emp.job_title || '-' }}</td>
                  <td>{{ emp.is_manager ? 'Oui' : 'Non' }}</td>
                  <td><span :class="['active-badge', emp.active ? 'yes' : 'no']">{{ emp.active ? 'Oui' : 'Non' }}</span></td>
                  <td>{{ emp.created_at || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

      <!-- Emails Tab -->
      <template v-if="activeTab === 'emails'">
        <div class="card card-pad">
          <div class="card-h">
            <h3>Emails</h3>
          </div>

          <div v-if="loadingEmails" style="text-align:center;padding:40px;color:var(--muted)">
            Chargement...
          </div>

          <div v-else-if="emails.length === 0" style="text-align:center;padding:40px;color:var(--muted)">
            Aucun email trouvé
          </div>

          <div v-else class="table-wrap">
            <table class="users-table emails-table">
              <thead>
                <tr>
                  <th>État</th>
                  <th>De</th>
                  <th>Objet</th>
                  <th>Aperçu</th>
                  <th>Date</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="email in emails" :key="email.id"
                    :class="{ 'email-unread': !email.is_read }"
                    @click="markAsRead(email.id)"
                    style="cursor:pointer">
                  <td>
                    <span :class="['read-badge', email.is_read ? 'read' : 'unread']">
                      {{ email.is_read ? 'Lu' : 'Non lu' }}
                    </span>
                  </td>
                  <td><b>{{ email.author_name }}</b></td>
                  <td>{{ email.subject }}</td>
                  <td class="email-body">{{ email.body }}</td>
                  <td>{{ email.date }}</td>
                  <td><span class="read-badge">{{ email.message_type }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

      <!-- Notifications Tab -->
      <template v-if="activeTab === 'notifications'">
        <div class="card card-pad">
          <div class="card-h">
            <h3>Notifications</h3>
          </div>

          <div v-if="loadingEmails" style="text-align:center;padding:40px;color:var(--muted)">
            Chargement...
          </div>

          <div v-else-if="notifications.length === 0" style="text-align:center;padding:40px;color:var(--muted)">
            Aucune notification trouvée
          </div>

          <div v-else class="table-wrap">
            <table class="users-table emails-table">
              <thead>
                <tr>
                  <th>État</th>
                  <th>De</th>
                  <th>Objet</th>
                  <th>Aperçu</th>
                  <th>Date</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="notif in notifications" :key="notif.id"
                    :class="{ 'email-unread': !notif.is_read }"
                    @click="markAsRead(notif.id)"
                    style="cursor:pointer">
                  <td>
                    <span :class="['read-badge', notif.is_read ? 'read' : 'unread']">
                      {{ notif.is_read ? 'Lu' : 'Non lu' }}
                    </span>
                  </td>
                  <td><b>{{ notif.author_name }}</b></td>
                  <td>{{ notif.subject }}</td>
                  <td class="email-body">{{ notif.body }}</td>
                  <td>{{ notif.date }}</td>
                  <td><span class="read-badge">{{ notif.message_type }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<style scoped>
.btn-logout {
  background: var(--red) !important;
}
.btn-logout:hover {
  background: white !important;
  color: var(--red) !important;
  border: 1px solid var(--red) !important;
}

.table-wrap {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.users-table th {
  text-align: left;
  padding: 10px 12px;
  background: var(--blue-soft);
  color: var(--navy);
  font-weight: 700;
  font-size: 12px;
  white-space: nowrap;
  border-bottom: 2px solid var(--line);
}

.users-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  white-space: nowrap;
}

.users-table tbody tr:hover {
  background: var(--blue-soft);
}

.role-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  text-transform: capitalize;
}

.role-badge.admin {
  background: var(--navy);
  color: #fff;
}

.role-badge.user {
  background: var(--blue-soft);
  color: var(--navy);
}

.active-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
}

.active-badge.yes {
  background: #e9f7ee;
  color: var(--green);
}

.active-badge.no {
  background: #fdecea;
  color: var(--red);
}

.email-unread {
  background: #f8faff;
}

.email-body {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--muted);
  font-size: 12px;
}

.read-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
}

.read-badge.unread {
  background: var(--blue-soft);
  color: var(--navy);
}

.read-badge.read {
  background: #f1f3f6;
  color: var(--muted);
}
</style>
