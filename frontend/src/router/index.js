import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'accueil', component: () => import('../views/Accueil.vue') },
  { path: '/directions', name: 'mesdirections', component: () => import('../views/MesDirections.vue') },
  // Page détaillée "riche" : correspond à la page-direction (Communication & Marketing) de la maquette
  { path: '/directions/comm', name: 'direction-comm', component: () => import('../views/Direction.vue') },
  {
    // équivalent de goDir(key) du mockup : une page générique alimentée par le param :key
    path: '/directions/:key',
    name: 'direction-generique',
    component: () => import('../views/DirectionGenerique.vue'),
    props: true
  },
  { path: '/helpdesk', name: 'helpdesk', component: () => import('../views/HelpDesk.vue') },
{  path: '/login',
  name: 'login',
  component: () => import('../views/Login.vue'),
  meta: {
    showSidebar: false,
    showTopbar: false,
    showFooter: false

  }
}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
