import {createRouter, createWebHistory} from 'vue-router'
import Home from '@/Home.vue'
import BeyCreation from '@/AddBey.vue'
import VerBey from '@/VerBey.vue'
import Registrar from '@/Registrar.vue'
import Inicio from '@/Inicio.vue'
import CrearChat from '@/CrearChatView.vue'
import ChatsView from '@/ChatsView.vue'
import ChatView from '@/ChatView.vue'
import SettingsView from '@/SettingsView.vue'
import PersonajesView from '@/PersonajesView.vue'
import VerPersonaje from '@/VerPersonaje.vue'
import CrearPersonajeView from '@/CrearPersonajeView.vue'
import PerfilView from '@/PerfilView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'index',
            component: Home
        },
        {
            path: '/home/:season?',
            name: 'Home',
            component: Home
        },
        {
            path: '/create/personaje',
            name: 'CrearPersonaje',
            component: CrearPersonajeView
        },
        {
            path: '/create/:nombre',
            name: 'Create',
            component: BeyCreation
        },
        {
            path: '/ver/:id',
            name: 'Ver',
            component: VerBey
        },
        {
            path: '/registro',
            name: 'Registro',
            component: Registrar
        },
        {
            path: '/iniciar',
            name: 'Iniciar',
            component: Inicio
        },
        {
            path: '/create/chat',
            name: 'Crear-chat',
            component: CrearChat
        },
        {
            path: '/chats',
            name: 'Chats',
            component: ChatsView
        },
        {
            path: '/chat/:id',
            name: 'Chat',
            component: ChatView
        },
        {
            path: '/settings',
            name: 'Settings',
            component: SettingsView
        },
        {
            path: '/perfil',
            name: 'Perfil',
            component: PerfilView
        },
        {
            path: '/personajes',
            name: 'Personajes',
            component: PersonajesView
        },
        {
            path: '/ver/personaje/:id',
            name: 'VerPersonaje',
            component: VerPersonaje
        }
    ]
})



export default router
