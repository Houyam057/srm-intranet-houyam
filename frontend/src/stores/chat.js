import { defineStore } from 'pinia'
import { ref } from 'vue'
import { odooApi } from '../api/odoo.js'

export const useChatStore = defineStore('chat', () => {
  const isOpen = ref(false)
  const isLoading = ref(false)
  const messages = ref([])
  const conversations = ref([])
  const currentConversationId = ref(null)
  const error = ref(null)

  function toggleChat() {
    isOpen.value = !isOpen.value
  }

  function openChat() {
    isOpen.value = true
  }

  function closeChat() {
    isOpen.value = false
  }

  function startNewConversation() {
    messages.value = []
    currentConversationId.value = null
    error.value = null
  }

  async function sendMessage(text) {
    if (!text.trim() || isLoading.value) return

    const userMessage = { role: 'user', content: text.trim() }
    messages.value.push(userMessage)
    isLoading.value = true
    error.value = null

    try {
      const payload = { message: text.trim() }
      if (currentConversationId.value) {
        payload.conversation_id = currentConversationId.value
      }

      const response = await odooApi.post('/api/chat', payload)
      const result = response.data

      if (result.success) {
        const assistantMessage = { role: 'assistant', content: result.data.response }
        messages.value.push(assistantMessage)
        currentConversationId.value = result.data.conversation_id
      } else {
        error.value = result.error || 'Une erreur est survenue'
        messages.value.push({
          role: 'assistant',
          content: 'Désolé, une erreur est survenue. Veuillez réessayer.',
        })
      }
    } catch (e) {
      error.value = e.response?.data?.error || e.message || 'Erreur de connexion'
      messages.value.push({
        role: 'assistant',
        content: 'Désolé, je ne peux pas me connecter au serveur. Veuillez réessayer.',
      })
    } finally {
      isLoading.value = false
    }
  }

  async function fetchConversations() {
    try {
      const response = await odooApi.get('/api/chat/history')
      conversations.value = response.data?.data?.conversations || []
    } catch {
      // silent
    }
  }

  async function loadConversation(conversationId) {
    try {
      const response = await odooApi.get('/api/chat/history', {
        params: { conversation_id: conversationId },
      })
      const data = response.data?.data?.conversation
      if (data) {
        messages.value = data.messages || []
        currentConversationId.value = data.id
        isOpen.value = true
      }
    } catch {
      // silent
    }
  }

  async function deleteConversation(conversationId) {
    try {
      await odooApi.delete(`/api/chat/conversation/${conversationId}`)
      conversations.value = conversations.value.filter(c => c.id !== conversationId)
      if (currentConversationId.value === conversationId) {
        startNewConversation()
      }
    } catch {
      // silent
    }
  }

  return {
    isOpen,
    isLoading,
    messages,
    conversations,
    currentConversationId,
    error,
    toggleChat,
    openChat,
    closeChat,
    startNewConversation,
    sendMessage,
    fetchConversations,
    loadConversation,
    deleteConversation,
  }
})
