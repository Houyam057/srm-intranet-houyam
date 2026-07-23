<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth.js'
import Sidebar from './components/Sidebar.vue'
import Topbar from './components/Topbar.vue'
import ChatWidget from './components/ChatWidget.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const authChecked = ref(false)

onMounted(async () => {
  await authStore.fetchUser()
  authChecked.value = true

  if (!authStore.isAuthenticated && route.name !== 'login') {
    router.push({ name: 'login' })
  }
})
</script>

<template>
  <div class="app">
    <template v-if="authChecked">
      <template v-if="authStore.isAuthenticated || route.name === 'login'">
        <Sidebar v-if="$route.meta.showSidebar !== false"/>

        <div class="main">
          <Topbar v-if="$route.meta.showTopbar !== false"/>

          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>

          <div class="footer"     v-if="$route.meta.showFooter !== false">
            <div class="safe">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>
              <span>La sécurité de tous,<br>notre priorité au quotidien.</span>
            </div>
            <div class="soc">
              <a><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v6h-4v-6a2 2 0 0 0-4 0v6h-4v-12h4v2a4 4 0 0 1 6-2"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
              <a><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg></a>
            </div>
            <div class="links">
              <span>&copy; 2026 SRM-TTA. Tous droits r&eacute;serv&eacute;s.</span>
              <a>Conditions d'utilisation</a>
              <a>Confidentialit&eacute;</a>
            </div>
          </div>
        </div>
      </template>
      <router-view v-else />
      <ChatWidget v-if="authStore.isAuthenticated" />
    </template>
  </div>
</template>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity .15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
