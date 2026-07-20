import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'accueil', component: () => import('../views/Accueil.vue') },
  { path: '/directions', name: 'mesdirections', component: () => import('../views/MesDirections.vue') },
  {path:'/profil', name:'profil', component: () => import('../views/Profile.vue')},
  // Page détaillée "riche" : correspond à la page-direction (Communication & Marketing) de la maquette
  { path: '/directions/comm', name: 'direction-comm', component: () => import('../views/Direction.vue') },
  { path : '/apps',name:'apps', component:() =>  import ('../views/Apps.vue')},
  { path : '/apps/sap', name:'sap',component:() => import ('../views/sap.vue')},
  { path : '/apps/sap-bi', name:'sap-bi',component:() => import ('../views/sap-bi.vue')},
  { path : '/apps/odoo', name:'odoo',component:() => import ('../views/Odoo.vue')},
  { path : '/formations-competences' , name :'formations-competences' ,component :() => import ('../views/Formation.vue')},
  { path : '/test',name:'test',component :()=> import('../views/Test.vue')},

  {
    // équivalent de goDir(key) du mockup : une page générique alimentée par le param :key
    path: '/directions/:key',
    name: 'direction-generique',
    component: () => import('../views/DirectionGenerique.vue'),
    props: true
  },
  { path: '/helpdesk', name: 'helpdesk', component: () => import('../views/HelpDesk.vue') },
  {path : '/flashinfo', name: 'flashinfo', component: () => import('../views/FlashInfo.vue')},
  {path: '/notre-societe', name: 'notre-societe', component: () => import('../views/NotreSociete.vue')},
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
