<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="topbar">
    <div class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input placeholder="Rechercher dans l'intranet..." />
      <kbd>Ctrl + K</kbd>
    </div>
    <div class="top-actions">
      <div class="ic-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>
        <span class="badge">3</span>
      </div>
      <div class="ic-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
        <span class="badge">5</span>
      </div>
      <div class="divider"></div>
      <div class="user" @click="handleLogout" style="cursor:pointer" title="Se déconnecter">
        <div class="av">{{ authStore.userInitials }}</div>
        <div><b>{{ authStore.userName || 'Utilisateur' }}</b><span>{{ authStore.user?.username || '' }}</span></div>
        <svg class="chev" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
      </div>
    </div>
  </div>
</template>
