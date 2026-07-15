<script setup>
import { useAuthStore } from '../stores/auth.js'

defineProps({
  tabs: { type: Array, required: true },
  modelValue: { type: String, required: true }
})

const emit = defineEmits(['update:modelValue'])
const authStore = useAuthStore()

function select(key) {
  emit('update:modelValue', key)
}
</script>

<template>
  <nav class="h-navbar">
    <div class="h-navbar-inner">
      <div class="h-nav-items">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['h-nav-item', { active: modelValue === tab.key }]"
          @click="select(tab.key)"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.h-navbar {
  display: inline-flex;
  background: var(--blue-soft);
  border-radius: 20px;
  padding: 4px;
  margin-bottom: 0;
  border: 1px solid var(--navy);
}

.h-navbar-inner {
  display: flex;
  align-items: center;
  gap: 8px;
}

.h-nav-items {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.h-nav-item {
  padding: 7px 14px;
  border: none;
  background: none;
  color: var(--navy);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  border-radius: 30px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.h-nav-item:hover {
  color: var(--muted);
  background: rgba(255, 255, 255, 0.1);
}

.h-nav-item.active {
  color: white;
  background: var(--navy);
  font-weight: 600;
}

.h-nav-user {
  background: #fff;
  color: #1a1a2e;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 30px;
  border: 2px solid #2a2a4a;
  white-space: nowrap;
  flex: none;
}
</style>
