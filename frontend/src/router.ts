import { createRouter, createWebHistory } from 'vue-router'
import ProgramsCatalog from './views/ProgramsCatalog.vue'
import ProgramDetails from './views/ProgramDetails.vue'
import CentersCatalog from './views/CentersCatalog.vue'
import CenterDetails from './views/CenterDetails.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/ProfilePage.vue'
import Favorites from './views/Favorites.vue'
import AdminPanel from './views/AdminPanel.vue'

  const r = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: ProgramsCatalog },
      { path: '/programs/:id', component: ProgramDetails },
      { path: '/centers', component: CentersCatalog },
      { path: '/centers/:id', component: CenterDetails },
      { path: '/login', component: Login },
      { path: '/register', component: Register },
      { path: '/profile', component: Profile },
      { path: '/favorites', component: Favorites },
      { path: '/admin', component: AdminPanel },
    ]
  })
  export default r
