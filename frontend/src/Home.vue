<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import api from './main';
import BeyComponent from '../components/BeyComponent.vue';
import Header from '../components/HeaderComponent.vue';
import BaseButton from '../components/BaseButton.vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const seleccion = computed(() => route.params.season || null);
const mostrandoSelectorTemporada = ref(false);

const beyblades = ref([]);
const busqueda = ref('');
const cargandoBeys = ref(false);

const user = localStorage.getItem('user');
const token = localStorage.getItem('auth_token');

const cargarBeys = async (select) => {
    const params = {};
    if (select && select.value) {
        params.select = select.value;
    }
    try {
        cargandoBeys.value = true;
        const res = await api.get('cargar/beyblade', { params });
        beyblades.value = res.data || [];
    } catch (error) {
        console.error('Error al cargar Beyblades:', error);
    } finally {
        cargandoBeys.value = false;
    }
};

const buscar = async () => {
    if (!busqueda.value.trim()) {
        if (seleccion.value) {
            await cargarBeys({ value: seleccion.value });
        }
        return;
    }
    try {
        cargandoBeys.value = true;
        const res = await api.get('buscador', {
            params: { busqueda: busqueda.value }
        });
        beyblades.value = res.data || [];
    } catch (error) {
        console.error('Error en búsqueda:', error);
    } finally {
        cargandoBeys.value = false;
    }
};

const irATemporadas = () => {
    mostrandoSelectorTemporada.value = true;
    router.push({ name: 'Home', query: { seasons: 'true' } });
};

const volverABienvenida = () => {
    mostrandoSelectorTemporada.value = false;
    router.push({ name: 'Home' });
};

watch(
    [() => route.params.season, () => route.query.seasons],
    ([newSeason, newSeasonsQuery]) => {
        if (newSeason) {
            cargarBeys({ value: newSeason });
            mostrandoSelectorTemporada.value = false;
        } else if (newSeasonsQuery === 'true') {
            mostrandoSelectorTemporada.value = true;
            beyblades.value = [];
        } else {
            mostrandoSelectorTemporada.value = false;
            beyblades.value = [];
        }
    },
    { immediate: true }
);

onMounted(() => {
    if (route.params.season) {
        cargarBeys({ value: route.params.season });
    } else if (route.query.seasons === 'true') {
        mostrandoSelectorTemporada.value = true;
    }
});
</script>

<template>
    <Header></Header>

    <!-- Main Container for Logged-In Users -->
    <div v-if="user && token" class="min-h-[calc(100vh-64px)] p-6 max-w-7xl mx-auto flex flex-col items-center">
        
        <!-- 1. WELCOME HUB (Default Home State) -->
        <div v-if="!seleccion && !mostrandoSelectorTemporada" class="w-full space-y-10 py-6 max-w-5xl">
            
            <!-- Hero Welcome Card -->
            <div class="glass-card relative overflow-hidden p-8 sm:p-12 rounded-3xl text-center flex flex-col items-center justify-center gap-5 shadow-2xl border border-white/30 dark:border-slate-700">
                <!-- Background Accent Glows -->
                <div class="absolute -top-24 -left-24 w-72 h-72 bg-amber-500/20 rounded-full blur-3xl pointer-events-none"></div>
                <div class="absolute -bottom-24 -right-24 w-72 h-72 bg-orange-600/20 rounded-full blur-3xl pointer-events-none"></div>

                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm">
                    <span>⚡ Portal Oficial BeyStory</span>
                </div>

                <h1 class="text-4xl sm:text-5xl font-black text-slate-900 dark:text-slate-100 tracking-tight leading-tight">
                    ¡Bienvenido a <span class="bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 bg-clip-text text-transparent">BeyStory</span>!
                </h1>

                <p class="text-sm sm:text-base text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
                    El universo definitivo de Beyblade Metal Fight. Explora a los Bladers legendarios, consulta el catálogo interactivo de Beyblades por temporadas y conecta con la comunidad.
                </p>
            </div>

            <!-- Direct Navigation Cards Grid (Unified Visual Style) -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full">
                
                <!-- Card 1: Personajes & Bladers -->
                <div class="glass-card flex flex-col justify-between p-6 rounded-3xl transition-all duration-300 hover:-translate-y-2 hover:border-amber-500 shadow-xl border border-white/30 dark:border-slate-700 group">
                    <div class="space-y-4">
                        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/40 flex items-center justify-center text-3xl shadow-inner group-hover:scale-110 transition-transform">
                            👤
                        </div>
                        <div>
                            <h2 class="text-2xl font-extrabold text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">
                                Bladers & Personajes
                            </h2>
                            <p class="text-xs text-slate-600 dark:text-slate-300 mt-2 leading-relaxed">
                                Explora las biografías, estadísticas de peso/altura y la evolución de los Beyblades asignados a cada Blader.
                            </p>
                        </div>
                    </div>

                    <div class="pt-6 mt-4 border-t border-slate-200 dark:border-slate-700/60">
                        <router-link 
                            to="/personajes"
                            class="w-full py-3 px-4 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center justify-center gap-2 no-underline"
                        >
                            <span>Explorar Personajes</span>
                            <span>→</span>
                        </router-link>
                    </div>
                </div>

                <!-- Card 2: Beyblades & Catálogo por Temporada -->
                <div class="glass-card flex flex-col justify-between p-6 rounded-3xl transition-all duration-300 hover:-translate-y-2 hover:border-amber-500 shadow-xl border border-white/30 dark:border-slate-700 group">
                    <div class="space-y-4">
                        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500/20 to-red-500/20 border border-orange-500/40 flex items-center justify-center text-3xl shadow-inner group-hover:scale-110 transition-transform">
                            🌀
                        </div>
                        <div>
                            <h2 class="text-2xl font-extrabold text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">
                                Beyblades por Temporada
                            </h2>
                            <p class="text-xs text-slate-600 dark:text-slate-300 mt-2 leading-relaxed">
                                Accede al catálogo completo dividido por sagas: Metal Fusion, Metal Masters, Metal Fury y sus piezas.
                            </p>
                        </div>
                    </div>

                    <div class="pt-6 mt-4 border-t border-slate-200 dark:border-slate-700/60">
                        <button 
                            type="button"
                            @click="irATemporadas"
                            class="w-full py-3 px-4 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer"
                        >
                            <span>Seleccionar Temporada</span>
                            <span>→</span>
                        </button>
                    </div>
                </div>

                <!-- Card 3: Chats & Comunidad -->
                <div class="glass-card flex flex-col justify-between p-6 rounded-3xl transition-all duration-300 hover:-translate-y-2 hover:border-amber-500 shadow-xl border border-white/30 dark:border-slate-700 group md:col-span-2 lg:col-span-1">
                    <div class="space-y-4">
                        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-red-500/20 to-amber-500/20 border border-red-500/40 flex items-center justify-center text-3xl shadow-inner group-hover:scale-110 transition-transform">
                            💬
                        </div>
                        <div>
                            <h2 class="text-2xl font-extrabold text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">
                                Chats & Comunidad
                            </h2>
                            <p class="text-xs text-slate-600 dark:text-slate-300 mt-2 leading-relaxed">
                                Entabla discusiones con otros fanáticos de Beyblade o consulta al asistente experto BeyBot.
                            </p>
                        </div>
                    </div>

                    <div class="pt-6 mt-4 border-t border-slate-200 dark:border-slate-700/60">
                        <router-link 
                            to="/chats"
                            class="w-full py-3 px-4 bg-gradient-to-r from-red-500 to-amber-500 hover:from-red-600 hover:to-amber-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center justify-center gap-2 no-underline"
                        >
                            <span>Ir a los Chats</span>
                            <span>→</span>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. SEASON SELECTOR STATE -->
        <div v-else-if="mostrandoSelectorTemporada && !seleccion" class="w-full flex flex-col justify-center items-center py-6 gap-8 max-w-5xl">
            <!-- Selector Header -->
            <div class="glass-card text-center px-8 py-5 rounded-2xl w-full max-w-3xl flex items-center justify-between gap-4">
                <div class="text-left">
                    <h1 class="font-extrabold text-2xl text-slate-900 dark:text-slate-100">🌀 Selecciona una Temporada</h1>
                    <p class="text-xs text-slate-600 dark:text-slate-300 mt-0.5">Elige una saga para explorar sus Beyblades correspondientes.</p>
                </div>
                <button 
                    type="button" 
                    @click="volverABienvenida"
                    class="px-3 py-1.5 bg-slate-500/15 hover:bg-slate-500/30 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition-colors flex items-center gap-1 cursor-pointer"
                >
                    <span>←</span> Bienvenida
                </button>
            </div>

            <!-- Season Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl px-4">
                <router-link :to="{name: 'Home', params:{season: 'Fusion'}}" class="group no-underline">
                    <div class="glass-card rounded-3xl p-3 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden space-y-3 border border-white/30 dark:border-slate-700 shadow-xl">
                        <img class="w-full h-48 object-cover rounded-2xl shadow-sm" :src="'/img/Beyblade_metal_fusion.webp'" alt="Metal Fusion">
                        <div class="text-center pb-2">
                            <h3 class="font-extrabold text-lg text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">Metal Fusion</h3>
                            <span class="text-xs text-amber-600 dark:text-amber-400 font-semibold">Temporada 1</span>
                        </div>
                    </div>
                </router-link>

                <router-link :to="{name: 'Home', params:{season: 'Masters'}}" class="group no-underline">
                    <div class="glass-card rounded-3xl p-3 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden space-y-3 border border-white/30 dark:border-slate-700 shadow-xl">
                        <img class="w-full h-48 object-cover rounded-2xl shadow-sm" :src="'/img/Beyblade_metal_masters.webp'" alt="Metal Masters">
                        <div class="text-center pb-2">
                            <h3 class="font-extrabold text-lg text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">Metal Masters</h3>
                            <span class="text-xs text-amber-600 dark:text-amber-400 font-semibold">Temporada 2</span>
                        </div>
                    </div>
                </router-link>

                <router-link :to="{name: 'Home', params:{season: 'Fury'}}" class="group no-underline">
                    <div class="glass-card rounded-3xl p-3 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden space-y-3 border border-white/30 dark:border-slate-700 shadow-xl">
                        <img class="w-full h-48 object-cover rounded-2xl shadow-sm" :src="'/img/Beyblade_Metal_Fury.png'" alt="Metal Fury">
                        <div class="text-center pb-2">
                            <h3 class="font-extrabold text-lg text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors">Metal Fury</h3>
                            <span class="text-xs text-amber-600 dark:text-amber-400 font-semibold">Temporada 3</span>
                        </div>
                    </div>
                </router-link>
            </div>

            <div class="flex justify-center mt-2">
                <div class="glass-card px-6 py-2.5 rounded-2xl">
                    <p class="text-xs font-semibold text-orange-600 dark:text-amber-400 text-center">✨ Próximamente más temporadas y sagas especiales</p>
                </div>
            </div>
        </div>

        <!-- 3. BEYBLADES GRID FOR SELECTED SEASON -->
        <div v-if="seleccion" class="w-full max-w-7xl space-y-6">
            <!-- Season Header & Search Bar -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 glass-card p-6 rounded-3xl shadow-xl">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">🌀</span>
                    <div>
                        <h1 class="font-extrabold text-2xl text-slate-900 dark:text-slate-100">Temporada: {{ seleccion }}</h1>
                        <p class="text-xs text-slate-600 dark:text-slate-300">Explora los Beyblades pertenecientes a la saga {{ seleccion }}.</p>
                    </div>
                </div>

                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <form @submit.prevent="buscar" class="flex items-center gap-2 flex-1 sm:flex-initial">
                        <input 
                            type="text" 
                            v-model="busqueda" 
                            placeholder="Buscar Beyblade..." 
                            class="w-full sm:w-64 px-4 py-2 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded-xl focus:outline-none focus:border-amber-500 transition-colors shadow-inner text-xs"
                        >
                        <button class="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-bold rounded-xl px-4 py-2 text-xs transition-all shadow-md cursor-pointer">
                            Buscar
                        </button>
                    </form>

                    <button 
                        @click="irATemporadas" 
                        class="bg-slate-500/15 hover:bg-slate-500/30 text-slate-700 dark:text-slate-300 px-3 py-2 rounded-xl text-xs font-bold transition-colors shadow-sm cursor-pointer flex items-center gap-1 flex-shrink-0"
                        title="Cambiar temporada"
                    >
                        <span>↺</span> Temporadas
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="cargandoBeys" class="glass-card p-8 rounded-2xl text-center text-slate-600 dark:text-slate-300 max-w-md mx-auto my-8">
                <div class="text-3xl animate-spin mb-2">🌀</div>
                <p class="font-semibold text-sm">Cargando Beyblades...</p>
            </div>

            <!-- Beyblades Cards Grid -->
            <div v-else-if="beyblades.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-2 justify-items-center">
                <div v-for="bey in beyblades" :key="bey.id" class="glass-card flex justify-center p-3 rounded-2xl transition-all duration-300 hover:-translate-y-1.5 hover:border-amber-500 overflow-hidden w-full max-w-xs shadow-lg">
                    <router-link class="no-underline text-slate-900 dark:text-slate-100 w-full" :to="{name: 'Ver', params:{id : bey.id}}" >
                        <BeyComponent
                            :photo="bey.photo"
                            :nombre="bey.nombre"
                            :color="bey.color"
                            :compact="true"
                        />
                    </router-link>
                </div>
            </div>

            <!-- Empty Beyblades State -->
            <div v-else class="glass-card p-8 rounded-3xl text-center max-w-md mx-auto my-8 space-y-3 shadow-xl">
                <span class="text-4xl">🌀</span>
                <h2 class="font-extrabold text-xl text-slate-900 dark:text-slate-100">No hay Beyblades en esta temporada</h2>
                <p class="text-xs text-slate-600 dark:text-slate-300">No se encontraron Beyblades registrados para {{ seleccion }}.</p>
            </div>
        </div>
    </div>

    <!-- Guest Unauthenticated Landing -->
    <div v-else class="relative min-h-[calc(100vh-64px)] flex items-center justify-center p-6">
        <div class="glass-card relative flex flex-col items-center text-center max-w-md p-8 rounded-3xl gap-5 shadow-2xl border border-white/30 dark:border-slate-700">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-3xl shadow-lg">
                ⚡
            </div>
            <div>
                <h1 class="font-black text-slate-900 dark:text-slate-100 text-2xl mb-1">Inicia sesión en BeyStory</h1>
                <p class="text-xs text-slate-600 dark:text-slate-300">Conéctate con otros Bladers y explora todo el universo Beyblade.</p>
            </div>
            <router-link to="/iniciar" class="w-full">
                <BaseButton color="#FF6B35" hoverColor="#E63946">Iniciar Sesión</BaseButton>
            </router-link>
            <div class="text-xs text-slate-600 dark:text-slate-400">
                <p>
                    ¿No estás registrado? 
                    <router-link to="/registro" class="text-orange-600 dark:text-amber-400 hover:text-red-600 dark:hover:text-amber-300 font-semibold underline ml-1">Regístrate aquí</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>

