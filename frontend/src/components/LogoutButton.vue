<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Adjust this path to match your project

const router = useRouter()
const authStore = useAuthStore()

// Keep track of loading state to prevent double-clicks
const isLoggingOut = ref(false)

async function handleLogout() {
  if (isLoggingOut.value) return
  
  isLoggingOut.value = true
  try {
    await authStore.logout()
    router.push({ name: 'login' })
  } catch (error) {
    console.error('Logout failed:', error)
    // Optional: Show an error notification to the user here
  } finally {
    isLoggingOut.value = false
  }
}
</script>

<template>
  <button 
    @click="handleLogout" 
    :disabled="isLoggingOut"
    class="logout-btn"
  >
    <span v-if="isLoggingOut">Logging out...</span>
    <span v-else>Logout</span>
  </button>
</template>

<style scoped>
.logout-btn {
  padding: 8px 16px;
  background-color: #e11d48; /* Red theme */
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.logout-btn:hover {
  background-color: white;
  color : var(--red);
}

.logout-btn:disabled {
  background-color: #fda4af;
  cursor: not-allowed;
}
</style>