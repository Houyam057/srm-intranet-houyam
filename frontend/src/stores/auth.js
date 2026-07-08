import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { odooApi } from '../api/odoo.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!user.value)
  const userName = computed(() => user.value?.name || '')
  const userInitials = computed(() => {
    if (!user.value?.name) return '??'
    return user.value.name
      .split(' ')
      .map(w => w[0])
      .slice(0, 2)
      .join('')
      .toUpperCase()
  })

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const db = import.meta.env.VITE_ODOO_DB || 'odoo'
      const response = await odooApi.post('/web/session/authenticate', {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          login: email,
          password: password,
          db: db
        },
        id: Date.now()
      })

      const result = response.data?.result
      if (result && result.uid) {
        user.value = {
          id: result.uid,
          name: result.name || result.username || email,
          username: result.username || email,
          partnerId: result.partner_id,
          companyId: result.company_id
        }
        return true
      } else {
        error.value = 'Identifiants incorrects'
        return false
      }
    } catch (e) {
      error.value = e.response?.data?.result?.error
        || e.message
        || 'Erreur de connexion au serveur'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    loading.value = true
    try {
      const response = await odooApi.post('/web/session/get_session_info', {
        jsonrpc: '2.0',
        method: 'call',
        params: {},
        id: Date.now()
      })

      const result = response.data?.result
      if (result && result.uid) {
        user.value = {
          id: result.uid,
          name: result.name || result.username,
          username: result.username,
          partnerId: result.partner_id,
          companyId: result.company_id
        }
      } else {
        user.value = null
      }
    } catch {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await odooApi.post('/web/session/destroy', {
        jsonrpc: '2.0',
        method: 'call',
        params: {},
        id: Date.now()
      })
    } finally {
      user.value = null
    }
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    userName,
    userInitials,
    login,
    fetchUser,
    logout
  }
})
