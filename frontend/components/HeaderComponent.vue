
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ModalSugerirComponent from './ModalSugerirComponent.vue'
import api from '../src/main'

const router = useRouter()
const open = ref(false)

const getStoredUser = () => {
    const raw = localStorage.getItem('user');
    if (!raw) return null;
    try {
        return typeof raw === 'string' && raw.startsWith('{') ? JSON.parse(raw) : { username: raw };
    } catch (e) {
        return { username: raw };
    }
};

const userObj = ref(getStoredUser());
const user = computed(() => userObj.value);

const esAdmin = computed(() => {
    return Boolean(userObj.value?.is_staff || userObj.value?.is_superuser);
});

const sincronizarPerfil = async () => {
    if (!userObj.value?.id) return;
    try {
        const res = await api.get(`perfil/usuario?user_id=${userObj.value.id}`);
        if (res.data) {
            const updated = { ...userObj.value, ...res.data };
            userObj.value = updated;
            localStorage.setItem('user', JSON.stringify(updated));
        }
    } catch (err) {
        console.error('Error al sincronizar perfil en header:', err);
    }
};

const mostrarModalSugerir = ref(false)
const tipoSugerencia = ref('beyblade')

const abrirSugerir = (tipo = 'beyblade') => {
    tipoSugerencia.value = tipo
    mostrarModalSugerir.value = true
    open.value = false
}

const logout = () => {
    try {
        localStorage.removeItem('user')
        localStorage.removeItem('auth_token')
        router.push('/home')
        window.location.reload()
    } catch(error) {
        console.error(error)
    }
}

onMounted(() => {
    sincronizarPerfil()
});
</script>


<template>
    <header class="header">
        <div class="flex items-center">
            <router-link class="flex items-center py-1 px-1 rounded-lg hover:opacity-90 transition-opacity" :to="{name: 'Home'}">
                <img class="h-10 w-auto object-contain" src="/img/BeyStory2.png" alt="BeyStory">
            </router-link>
        </div>

        <nav v-if="user" class="opciones">
            <!-- Inline desktop navigation links (hidden on mobile) -->
            <div class="hidden md:flex items-center gap-1">
                <router-link class="nav-link" :to="{name: 'Home'}">Inicio</router-link>
                <router-link class="nav-link" :to="{name: 'Personajes'}">Personajes</router-link>
                <router-link class="nav-link" :to="{name: 'Home', query: {seasons: 'true'}}">Beyblades</router-link>
                <router-link class="nav-link" :to="{name: 'Chats'}">Chats</router-link>
                <button type="button" @click="logout" class="nav-link">LogOut</button>
            </div>

            <!-- Hamburger Button -->
            <button 
                type="button" 
                @click="open = !open" 
                class="flex items-center justify-center w-10 h-10 bg-white/10 hover:bg-white/20 text-white rounded-xl transition-all border border-white/20 shadow-sm active:scale-95 cursor-pointer z-50 ml-2"
                aria-label="Abrir menú"
            >
                <span class="text-lg font-bold">{{ open ? '✕' : '☰' }}</span>
            </button>

            <!-- Backdrop for Mobile & Desktop overlay -->
            <div 
                v-if="open" 
                @click="open = false" 
                class="fixed inset-0 bg-black/50 backdrop-blur-xs z-40 transition-opacity"
            ></div>

            <!-- Dropdown Menu -->
            <transition
                enter-active-class="transition transform duration-300 ease-out"
                enter-from-class="translate-x-full opacity-0 scale-95"
                enter-to-class="translate-x-0 opacity-100 scale-100"
                leave-active-class="transition transform duration-200 ease-in"
                leave-from-class="translate-x-0 opacity-100 scale-100"
                leave-to-class="translate-x-full opacity-0 scale-95"
            >
                <div 
                    v-if="open" 
                    class="fixed top-16 right-3 sm:right-6 w-72 max-w-[calc(100vw-1.5rem)] max-h-[calc(100vh-5rem)] bg-slate-900/95 border border-slate-700/80 shadow-2xl rounded-2xl p-4 backdrop-blur-xl z-50 flex flex-col gap-1 overflow-y-auto text-slate-100"
                >
                    <!-- Mobile Navigation Links Section (only visible on mobile screens < md) -->
                    <div class="md:hidden space-y-1 pb-2">
                        <div class="px-3 py-1 text-[11px] font-extrabold uppercase tracking-wider text-amber-500/80">
                            Navegación
                        </div>
                        <router-link 
                            @click="open = false"
                            class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-sm font-semibold flex items-center gap-2.5" 
                            :to="{name: 'Home'}"
                        >
                            <span>🏠</span> Inicio
                        </router-link>
                        <router-link 
                            @click="open = false"
                            class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-sm font-semibold flex items-center gap-2.5" 
                            :to="{name: 'Personajes'}"
                        >
                            <span>👥</span> Personajes
                        </router-link>
                        <router-link 
                            @click="open = false"
                            class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-sm font-semibold flex items-center gap-2.5" 
                            :to="{name: 'Home', query: {seasons: 'true'}}"
                        >
                            <span>🌀</span> Beyblades
                        </router-link>
                        <router-link 
                            @click="open = false"
                            class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-sm font-semibold flex items-center gap-2.5" 
                            :to="{name: 'Chats'}"
                        >
                            <span>💬</span> Chats
                        </router-link>
                        <div class="my-1 border-t border-slate-700/60"></div>
                    </div>

                    <!-- Creation Options Section (ADMIN ONLY) -->
                    <template v-if="esAdmin">
                        <div class="px-3 py-1 text-[11px] font-extrabold uppercase tracking-wider text-amber-500/80">
                            Crear & Añadir (Admin)
                        </div>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'bey'}}">Crear Beyblade</router-link>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'fusion'}}">Crear Fusion Wheel</router-link>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'clear'}}">Crear Clear Wheel</router-link>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'track'}}">Crear Spin Track</router-link>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'tip'}}">Crear Tip</router-link>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium" :to="{name: 'Create', params: {nombre: 'tipe'}}">Crear Type</router-link>

                        <div class="my-1 border-t border-slate-700/60"></div>
                        <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium flex items-center gap-2" :to="{name: 'CrearPersonaje'}">
                            <span>👤</span> Crear Personaje
                        </router-link>
                    </template>

                    <!-- Suggestions / Reports Section (FOR NORMAL USERS) -->
                    <template v-else>
                        <div class="px-3 py-1 text-[11px] font-extrabold uppercase tracking-wider text-amber-500/80">
                            Sugerencias
                        </div>
                        <button 
                            type="button"
                            @click="abrirSugerir('beyblade')" 
                            class="w-full text-left px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium flex items-center gap-2 cursor-pointer"
                        >
                            <span>💡</span> Sugerir Beyblade
                        </button>
                        <button 
                            type="button"
                            @click="abrirSugerir('personaje')" 
                            class="w-full text-left px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium flex items-center gap-2 cursor-pointer"
                        >
                            <span>💡</span> Sugerir Personaje
                        </button>
                    </template>

                    <div class="my-1 border-t border-slate-700/60"></div>

                    <!-- User Account & Reports Section -->
                    <div class="px-3 py-1 text-[11px] font-extrabold uppercase tracking-wider text-amber-500/80">
                        Cuenta & Administración
                    </div>
                    <router-link v-if="esAdmin" @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-semibold flex items-center gap-2" :to="{name: 'UsersView'}">
                        <span>👥</span> Gestión de Usuarios
                    </router-link>
                    <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-semibold flex items-center gap-2" :to="{name: 'Reportes'}">
                        <span>📋</span> {{ esAdmin ? 'Gestionar Reportes' : 'Mis Sugerencias' }}
                    </router-link>
                    <router-link @click="open = false" class="block px-3.5 py-2 text-amber-400 hover:text-amber-300 hover:bg-white/10 rounded-xl transition-colors text-xs font-semibold flex items-center gap-2" :to="{name: 'Perfil'}">
                        <span>👤</span> Mi Perfil
                    </router-link>

                    <router-link @click="open = false" class="block px-3.5 py-2 text-slate-200 hover:text-amber-400 hover:bg-white/10 rounded-xl transition-colors text-xs font-medium flex items-center gap-2" :to="{name: 'Settings'}">
                        <span>⚙️</span> Settings
                    </router-link>

                    <!-- Mobile LogOut Button -->
                    <div class="md:hidden pt-1 border-t border-slate-700/60">
                        <button 
                            type="button" 
                            @click="logout(); open = false;" 
                            class="w-full text-left px-3.5 py-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-xl transition-colors text-xs font-bold flex items-center gap-2 cursor-pointer"
                        >
                            <span>🚪</span> Cerrar Sesión
                        </button>
                    </div>
                </div>
            </transition>
        </nav>
    </header>

    <!-- Suggestion Modal -->
    <ModalSugerirComponent 
        v-if="mostrarModalSugerir" 
        :tipo="tipoSugerencia" 
        @cerrar="mostrarModalSugerir = false" 
    />
</template>


<style scoped>
    .header {
        display: flex;
        background: linear-gradient(135deg, rgba(230, 57, 70, 0.85) 0%, rgba(255, 107, 53, 0.85) 50%, rgba(255, 165, 0, 0.85) 100%);
        align-items: center;
        justify-content: space-between;
        height: 64px;
        padding: 0 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3), inset 0 -1px 0 0 rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 40;
    }

    @media (min-width: 640px) {
        .header {
            padding: 0 24px;
        }
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




