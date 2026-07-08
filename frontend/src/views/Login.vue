<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const errorMsg = ref('')

async function handleSubmit() {
  errorMsg.value = ''
  const success = await authStore.login(form.email, form.password)
  if (success) {
    router.push({ name: 'accueil' })
  } else {
    errorMsg.value = authStore.error || 'Identifiants incorrects'
  }
}
</script>

<template>
    <div class="box">
        <div class="content">
            <img src="../assets/logo.png" alt="Logo" class="logo">
            <h1 style="text-align: center;">Bienvenue sur le portail SRM-TTA</h1>
            <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                      <label class="floating-label" style="margin-top: 20px;">
                          <span>Email</span>
                             <input v-model="form.email" name="Email" type="text" required
                                  placeholder="Email" />
                      </label>
              </div>
              <div class="form-group">
                      <label class="floating-label" style="margin-top:25px;">
                          <span>Mot de passe</span>
                             <input v-model="form.password" name="Password" type="password" required
                                  placeholder="Mot de passe" />
                      </label>
              </div>
              <button type="submit" class="btn btn-primary" style="margin-top: 30px; width: 100%;" :disabled="authStore.loading">
                {{ authStore.loading ? 'Connexion en cours...' : 'Se connecter' }}
              </button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                <a href="/" style="text-decoration: underline;">Mot de passe oublié ?</a>
            </p>
        </div>
    </div>
</template>

<style scoped>
.content {
    min-height: 500px;
    min-width: 500px;
    padding: 20px 22px;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);

    display: flex;
    flex-direction: column;
}

.box {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.logo {
    display: block;
    width: 150px;
    height: 130px;
    object-fit: contain;
    margin: 0 auto 30px auto;
}

.error-msg {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 16px;
    font-size: 0.9rem;
    text-align: center;
}
</style>
