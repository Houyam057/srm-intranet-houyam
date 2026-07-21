import { defineStore } from 'pinia'
import { ref } from 'vue'

// Etat partage entre Topbar (bouton menu) et Sidebar (le menu lui-meme),
// utilise uniquement en dessous de 1150px (voir @media dans main.css).
export const useUiStore = defineStore('ui', () => {
  const sidebarOpen = ref(false)

  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function closeSidebar() {
    sidebarOpen.value = false
  }

  return { sidebarOpen, toggleSidebar, closeSidebar }
})
