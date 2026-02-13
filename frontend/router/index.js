import {createRouter, createWebHistory} from 'vue-router'
import Home from '@/Home.vue'
import BeyCreation from '@/AddBey.vue'
import VerBey from '@/VerBey.vue'
import Registrar from '@/Registrar.vue'
import Inicio from '@/Inicio.vue'
import CrearChat from '@/CrearChatView.vue'
import ChatsView from '@/ChatsView.vue'
import ChatView from '@/ChatView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'index',
            component: Home
        },
        {
            path: '/home',
            name: 'Home',
            component: Home
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
        }
    ]
})

export default router