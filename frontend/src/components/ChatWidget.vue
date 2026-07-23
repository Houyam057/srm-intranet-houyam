<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'
import { useChatStore } from '../stores/chat.js'
import { MessageCircle, X, Send, Trash2, Plus, Bot, User } from 'lucide-vue-next'

const chatStore = useChatStore()
const inputMessage = ref('')
const messagesContainer = ref(null)
const showHistory = ref(false)

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(() => chatStore.messages.length, scrollToBottom)

async function handleSend() {
  const msg = inputMessage.value.trim()
  if (!msg) return
  inputMessage.value = ''
  await chatStore.sendMessage(msg)
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

onMounted(() => {
  chatStore.fetchConversations()
})

function toggleHistory() {
  showHistory.value = !showHistory.value
  if (showHistory.value) {
    chatStore.fetchConversations()
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="chat-widget">
    <!-- Bulle flottante -->
    <button class="chat-bubble" @click="chatStore.toggleChat()" :class="{ active: chatStore.isOpen }">
      <MessageCircle v-if="!chatStore.isOpen" :size="24" />
      <X v-else :size="24" />
    </button>

    <!-- Panneau de chat -->
    <Transition name="chat-panel">
      <div v-if="chatStore.isOpen" class="chat-panel">
        <!-- Header -->
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar">
              <Bot :size="20" />
            </div>
            <div>
              <h4>Assistant IA</h4>
              <span class="status">En ligne</span>
            </div>
          </div>
          <div class="chat-header-actions">
            <button class="header-btn" @click="toggleHistory" title="Historique">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
            </button>
            <button class="header-btn" @click="chatStore.startNewConversation()" title="Nouvelle conversation">
              <Plus :size="18" />
            </button>
            <button class="header-btn" @click="chatStore.closeChat()" title="Fermer">
              <X :size="18" />
            </button>
          </div>
        </div>

        <!-- Historique sidebar -->
        <div v-if="showHistory" class="chat-history">
          <div class="history-header">
            <span>Conversations</span>
          </div>
          <div v-if="chatStore.conversations.length === 0" class="history-empty">
            Aucune conversation
          </div>
          <div
            v-for="conv in chatStore.conversations"
            :key="conv.id"
            class="history-item"
            @click="chatStore.loadConversation(conv.id); showHistory = false"
          >
            <div class="history-item-content">
              <span class="history-title">{{ conv.name }}</span>
              <span class="history-date">{{ formatDate(conv.updated_at) }}</span>
            </div>
            <button class="history-delete" @click.stop="chatStore.deleteConversation(conv.id)">
              <Trash2 :size="14" />
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div class="chat-messages" ref="messagesContainer">
          <div v-if="chatStore.messages.length === 0" class="chat-welcome">
            <div class="welcome-icon">
              <Bot :size="32" />
            </div>
            <h4>Bonjour !</h4>
            <p>Je suis votre assistant IA. Posez-moi vos questions sur l'entreprise, les employés, les documents, ou les actualités.</p>
            <div class="welcome-suggestions">
              <button @click="chatStore.sendMessage('Qui sont les employés de mon département ?')">
                Qui sont les employés de mon département ?
              </button>
              <button @click="chatStore.sendMessage('Quelles sont les dernières actualités ?')">
                Quelles sont les dernières actualités ?
              </button>
              <button @click="chatStore.sendMessage('Quels documents sont disponibles ?')">
                Quels documents sont disponibles ?
              </button>
            </div>
          </div>

          <div
            v-for="(msg, index) in chatStore.messages"
            :key="index"
            class="chat-message"
            :class="msg.role"
          >
            <div class="message-avatar">
              <User v-if="msg.role === 'user'" :size="16" />
              <Bot v-else :size="16" />
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(msg.content)"></div>
            </div>
          </div>

          <div v-if="chatStore.isLoading" class="chat-message assistant">
            <div class="message-avatar">
              <Bot :size="16" />
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="chat-input">
          <textarea
            v-model="inputMessage"
            @keydown="handleKeydown"
            placeholder="Tapez votre message..."
            rows="1"
            :disabled="chatStore.isLoading"
          />
          <button
            class="send-btn"
            @click="handleSend"
            :disabled="!inputMessage.trim() || chatStore.isLoading"
          >
            <Send :size="18" />
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
export default {
  methods: {
    formatMessage(text) {
      if (!text) return ''
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
    }
  }
}
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  font-family: "Segoe UI", Inter, Roboto, -apple-system, sans-serif;
}

/* Bulle */
.chat-bubble {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--navy, #0f2f6b), var(--blue, #1f5fd6));
  color: #fff;
  border: none;
  cursor: pointer;
  display: grid;
  place-items: center;
  box-shadow: 0 4px 16px rgba(15, 47, 107, 0.35);
  transition: all 0.3s ease;
}

.chat-bubble:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(15, 47, 107, 0.45);
}

.chat-bubble.active {
  background: linear-gradient(135deg, #dc3545, #c82333);
}

/* Panneau */
.chat-panel {
  position: absolute;
  bottom: 72px;
  right: 0;
  width: 400px;
  height: 560px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(15, 47, 107, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--line, #e7ecf3);
}

/* Transition */
.chat-panel-enter-active,
.chat-panel-leave-active {
  transition: all 0.3s ease;
}
.chat-panel-enter-from,
.chat-panel-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.95);
}

/* Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: linear-gradient(135deg, var(--navy, #0f2f6b), var(--blue, #1f5fd6));
  color: #fff;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: grid;
  place-items: center;
}

.chat-header h4 {
  font-size: 14px;
  font-weight: 700;
  margin: 0;
}

.status {
  font-size: 11px;
  opacity: 0.8;
}

.chat-header-actions {
  display: flex;
  gap: 4px;
}

.header-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.2s;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Historique */
.chat-history {
  border-bottom: 1px solid var(--line, #e7ecf3);
  max-height: 200px;
  overflow-y: auto;
}

.history-header {
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 700;
  color: var(--muted, #6b7a90);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-empty {
  padding: 16px;
  text-align: center;
  color: var(--muted, #6b7a90);
  font-size: 13px;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s;
}

.history-item:hover {
  background: var(--blue-soft, #eef3fc);
}

.history-item-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.history-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--ink, #12233f);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-date {
  font-size: 11px;
  color: var(--muted, #6b7a90);
}

.history-delete {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--muted, #6b7a90);
  cursor: pointer;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.history-delete:hover {
  background: #fee;
  color: #dc3545;
}

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 24px 16px;
  color: var(--ink, #12233f);
}

.welcome-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--blue-soft, #eef3fc), #dbe7fa);
  display: grid;
  place-items: center;
  color: var(--navy, #0f2f6b);
  margin-bottom: 12px;
}

.chat-welcome h4 {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 6px;
}

.chat-welcome p {
  font-size: 13px;
  color: var(--muted, #6b7a90);
  max-width: 280px;
  line-height: 1.5;
  margin: 0 0 16px;
}

.welcome-suggestions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  max-width: 280px;
}

.welcome-suggestions button {
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid var(--line, #e7ecf3);
  background: #fff;
  color: var(--ink, #12233f);
  font-size: 12.5px;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
}

.welcome-suggestions button:hover {
  background: var(--blue-soft, #eef3fc);
  border-color: var(--blue, #1f5fd6);
  color: var(--navy, #0f2f6b);
}

/* Message */
.chat-message {
  display: flex;
  gap: 8px;
  max-width: 85%;
}

.chat-message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.chat-message.assistant .message-avatar {
  background: linear-gradient(135deg, var(--blue-soft, #eef3fc), #dbe7fa);
  color: var(--navy, #0f2f6b);
}

.chat-message.user .message-avatar {
  background: linear-gradient(135deg, var(--navy, #0f2f6b), var(--blue, #1f5fd6));
  color: #fff;
}

.message-content {
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 13.5px;
  line-height: 1.5;
}

.chat-message.assistant .message-content {
  background: var(--blue-soft, #eef3fc);
  color: var(--ink, #12233f);
  border-bottom-left-radius: 4px;
}

.chat-message.user .message-content {
  background: linear-gradient(135deg, var(--navy, #0f2f6b), var(--blue, #1f5fd6));
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message-text :deep(code) {
  background: rgba(0, 0, 0, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--navy, #0f2f6b);
  opacity: 0.4;
  animation: typing 1.2s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { opacity: 0.4; transform: translateY(0); }
  30% { opacity: 1; transform: translateY(-4px); }
}

/* Input */
.chat-input {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--line, #e7ecf3);
  background: #fff;
}

.chat-input textarea {
  flex: 1;
  border: 1px solid var(--line, #e7ecf3);
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 13.5px;
  font-family: inherit;
  resize: none;
  outline: none;
  max-height: 100px;
  line-height: 1.4;
  transition: border-color 0.2s;
}

.chat-input textarea:focus {
  border-color: var(--blue, #1f5fd6);
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, var(--navy, #0f2f6b), var(--blue, #1f5fd6));
  color: #fff;
  cursor: pointer;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 480px) {
  .chat-panel {
    width: calc(100vw - 32px);
    height: calc(100vh - 120px);
    right: -8px;
  }
}
</style>
