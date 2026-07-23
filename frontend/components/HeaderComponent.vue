
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const open = ref(false)
const user = localStorage.getItem('user')

const logout = () => {
    try {
        if (user) {
            localStorage.removeItem('user')
            localStorage.removeItem('auth_token')
        }
        router.push('/home')
        window.location.reload()
    } catch(error) {
        console.error(error)
    }
}
</script>

<template>
    <header class="header">
        <div class="flex items-center">
            <router-link class="flex items-center py-1 px-1 rounded-lg hover:opacity-90 transition-opacity" :to="{name: 'Home'}">
                <img class="h-10 w-auto object-contain" src="/img/BeyStory2.png" alt="BeyStory">
            </router-link>
        </div>
        <nav v-if="user" class="opciones">
            <transition
                enter-active-class="transition transform duration-300 ease-out"
                enter-from-class="translate-x-full opacity-0"
                enter-to-class="translate-x-0 opacity-100"
                leave-active-class="transition transform duration-300 ease-in"
                leave-from-class="translate-x-0 opacity-100"
                leave-to-class="translate-x-full opacity-0"
            >
                <div v-if="open" class="fixed top-16 right-4 w-64 bg-slate-900/95 border border-slate-700/60 shadow-2xl rounded-xl p-4 backdrop-blur-md z-50 flex flex-col gap-1">
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'bey'}}">Crear Beyblade</router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'fusion'}}">Crear Fusion Wheel</router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'clear'}}">Crear Clear Wheel</router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'track'}}">Crear Spin track</router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'tip'}}">Crear Tip</router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium" :to="{name: 'Create', params: {nombre: 'tipe'}}">Crear Tipe</router-link>
                    <div class="my-1 border-t border-slate-700/60"></div>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium flex items-center gap-2" :to="{name: 'CrearPersonaje'}">
                        <span>👤</span> Crear Personaje
                    </router-link>
                    <div class="my-1 border-t border-slate-700/60"></div>
                    <router-link class="block px-4 py-2.5 text-amber-400 hover:text-amber-300 hover:bg-white/5 rounded-lg transition-colors text-sm font-semibold flex items-center gap-2" :to="{name: 'Perfil'}">
                        <span>👤</span> Mi Perfil
                    </router-link>
                    <router-link class="block px-4 py-2.5 text-slate-200 hover:text-amber-400 hover:bg-white/5 rounded-lg transition-colors text-sm font-medium flex items-center gap-2" :to="{name: 'Settings'}">
                        <span>⚙️</span> Settings
                    </router-link>
                </div>



            </transition>
            
            <router-link class="nav-link" :to="{name: 'Home'}">Inicio</router-link>
            <router-link class="nav-link" :to="{name: 'Personajes'}">Personajes</router-link>
            <router-link class="nav-link" :to="{name: 'Home', query: {seasons: 'true'}}">Beyblades</router-link>
            <router-link class="nav-link" :to="{name: 'Chats'}">Chats</router-link>
            <button type="button" @click="logout" class="nav-link">LogOut</button>
            <button type="button" @click="open = !open" class="flex items-center justify-center w-9 h-9 ml-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors">☰</button>

        </nav>
    </header>
</template>


<style scoped>
    .header {
        display: flex;
        background: linear-gradient(135deg, rgba(230, 57, 70, 0.85) 0%, rgba(255, 107, 53, 0.85) 50%, rgba(255, 165, 0, 0.85) 100%);
        align-items: center;
        justify-content: space-between;
        height: 64px;
        padding: 0 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3), inset 0 -1px 0 0 rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 40;
    }

    .opciones {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .nav-link {
        text-decoration: none;
        color: white;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.2s ease;
        padding: 8px 14px;
        border-radius: 8px;
        background: transparent;
        border: none;
        cursor: pointer;
    }

    .nav-link:hover {
        color: #FFF;
        background: rgba(255, 255, 255, 0.25);
    }
</style>



