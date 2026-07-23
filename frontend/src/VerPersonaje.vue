<script setup>
import Header from '../components/HeaderComponent.vue';
import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
import ModalEditarPersonajeComponent from '../components/ModalEditarPersonajeComponent.vue';
import ModalSugerirComponent from '../components/ModalSugerirComponent.vue';
import api from './main';
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const personaje = ref(null);
const cargando = ref(true);

const mostrarModalEditar = ref(false);
const mostrarModalEliminar = ref(false);
const mostrarModalSugerir = ref(false);
const eliminando = ref(false);

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;
const esAdmin = computed(() => localUser?.is_staff || localUser?.is_superuser || false);

const cargarPersonaje = async (targetId = route.params.id) => {
    if (!targetId) return;
    try {
        cargando.value = true;
        const res = await api.get(`cargar/personaje/${targetId}`);
        personaje.value = res.data;
        console.log('Detalle de personaje:', personaje.value);
    } catch (error) {
        console.error('Error al cargar detalle de personaje:', error);
    } finally {
        cargando.value = false;
    }
};

const eliminarPersonaje = async () => {
    if (!personaje.value) return;
    try {
        eliminando.value = true;
        await api.post(`eliminar/personaje/${personaje.value.id}`);
        mostrarModalEliminar.value = false;
        router.push('/personajes');
    } catch (error) {
        console.error('Error al eliminar personaje:', error);
    } finally {
        eliminando.value = false;
    }
};

const activeBeyblades = computed(() => {
    if (!personaje.value) return [];
    if (personaje.value.beyblades && personaje.value.beyblades.length > 0) {
        return personaje.value.beyblades;
    }
    if (personaje.value.beyblade) {
        return [personaje.value.beyblade];
    }
    return [];
});

const getBeyImage = (photo) => {
    if (!photo) return '/img/image.png';
    if (photo.startsWith('http')) return photo;
    return `https://project-bey-production.up.railway.app${photo}`;
};

watch(
    () => route.params.id,
    (newId) => {
        if (newId) {
            cargarPersonaje(newId);
        }
    }
);

onMounted(() => {
    cargarPersonaje();
});
</script>

<template>
    <Header></Header>

    <div class="flex flex-col items-center justify-center p-6 max-w-5xl mx-auto min-h-[calc(100vh-64px)] space-y-8">
        <!-- Loading State -->
        <div v-if="cargando" class="glass-card p-8 rounded-2xl text-center text-slate-600 dark:text-slate-300 max-w-md w-full">
            <div class="text-3xl animate-spin mb-2">🌀</div>
            <p class="font-semibold text-sm">Cargando información del personaje...</p>
        </div>

        <!-- Not Found State -->
        <div v-else-if="!personaje" class="glass-card p-8 rounded-2xl text-center text-slate-600 dark:text-slate-300 max-w-md w-full">
            <h2 class="font-bold text-xl mb-2">Personaje no encontrado</h2>
            <router-link to="/personajes" class="text-amber-500 font-semibold underline">Volver a personajes</router-link>
        </div>

        <div v-else class="w-full space-y-8">
            <!-- Character Header Card -->
            <div class="glass-card flex flex-col md:flex-row items-center gap-8 p-8 rounded-3xl w-full shadow-2xl relative">
                <!-- Action Buttons Top Corner -->
                <div class="absolute top-4 right-4 flex items-center gap-2">
                    <template v-if="esAdmin">
                        <button 
                            type="button" 
                            @click="mostrarModalEditar = true" 
                            class="px-3 py-1.5 bg-amber-500/15 hover:bg-amber-500 text-amber-600 dark:text-amber-300 hover:text-white border border-amber-500/40 rounded-xl text-xs font-bold transition-all flex items-center gap-1 cursor-pointer shadow-sm"
                            title="Editar personaje"
                        >
                            <span>✏️</span> Editar
                        </button>
                        <button 
                            type="button" 
                            @click="mostrarModalEliminar = true" 
                            class="px-3 py-1.5 bg-red-500/15 hover:bg-red-500 text-red-600 dark:text-red-300 hover:text-white border border-red-500/40 rounded-xl text-xs font-bold transition-all flex items-center gap-1 cursor-pointer shadow-sm"
                            title="Eliminar personaje"
                        >
                            <span>🗑️</span> Eliminar
                        </button>
                    </template>
                    <button 
                        v-else
                        type="button" 
                        @click="mostrarModalSugerir = true" 
                        class="px-3.5 py-1.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center gap-1 cursor-pointer"
                    >
                        <span>💡</span> Sugerir Cambio
                    </button>
                </div>


                <!-- Character Image -->
                <div class="relative w-56 h-56 rounded-2xl overflow-hidden border-2 border-white/40 dark:border-slate-700 bg-black/20 flex items-center justify-center flex-shrink-0 shadow-lg">
                    <img 
                        v-if="personaje.foto" 
                        :src="personaje.foto.startsWith('http') ? personaje.foto : `https://project-bey-production.up.railway.app${personaje.foto}`" 
                        :alt="personaje.nombre"
                        class="w-full h-full object-cover"
                    >
                    <span v-else class="text-7xl">👤</span>
                </div>

                <!-- Character Info & Details -->
                <div class="flex-1 space-y-4 text-slate-900 dark:text-slate-100 pr-16">
                    <div>
                        <h1 class="text-3xl font-extrabold text-slate-900 dark:text-slate-100 mb-1">{{ personaje.nombre }}</h1>
                        <div class="flex flex-wrap gap-2 mt-2">
                            <span v-if="personaje.altura" class="px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-semibold">
                                📏 Altura: {{ personaje.altura }}
                            </span>
                            <span v-if="personaje.peso" class="px-3 py-1 bg-orange-500/15 border border-orange-500/40 text-orange-600 dark:text-orange-400 rounded-full text-xs font-semibold">
                                ⚖️ Peso: {{ personaje.peso }}
                            </span>
                        </div>
                    </div>

                    <div v-if="personaje.personalidad" class="space-y-1">
                        <h3 class="font-bold text-sm text-orange-600 dark:text-amber-400 uppercase tracking-wider">Personalidad</h3>
                        <p class="text-sm leading-relaxed text-slate-700 dark:text-slate-300 bg-white/40 dark:bg-slate-800/50 p-3 rounded-xl border border-white/30 dark:border-slate-700/50">
                            {{ personaje.personalidad }}
                        </p>
                    </div>

                    <div v-if="personaje.historia" class="space-y-1">
                        <h3 class="font-bold text-sm text-orange-600 dark:text-amber-400 uppercase tracking-wider">Historia</h3>
                        <p class="text-sm leading-relaxed text-slate-700 dark:text-slate-300 bg-white/40 dark:bg-slate-800/50 p-3 rounded-xl border border-white/30 dark:border-slate-700/50">
                            {{ personaje.historia }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Associated Beyblades Section -->
            <div class="glass-card p-8 rounded-3xl w-full shadow-2xl space-y-6">
                <div class="border-b border-slate-200 dark:border-slate-700 pb-3 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <span class="text-2xl">⚡</span>
                        <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100">Beyblades Asignados</h2>
                    </div>
                    <span class="px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-semibold">
                        {{ activeBeyblades.length }} {{ activeBeyblades.length === 1 ? 'Beyblade' : 'Beyblades' }}
                    </span>
                </div>

                <div v-if="activeBeyblades.length === 0" class="text-center py-6 text-slate-500 dark:text-slate-400">
                    Este personaje no tiene ningún Beyblade asignado actualmente.
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    <!-- Clickable Minimal Beyblade Cards -->
                    <router-link 
                        v-for="bey in activeBeyblades"
                        :key="bey.id"
                        :to="{ name: 'Ver', params: { id: bey.id } }"
                        class="group flex items-center gap-4 p-4 bg-white/50 dark:bg-slate-800/60 border-2 border-amber-500/40 hover:border-amber-500 rounded-2xl transition-all duration-300 hover:scale-[1.03] shadow-lg hover:shadow-2xl no-underline text-slate-900 dark:text-slate-100 cursor-pointer"
                    >
                        <div class="w-24 h-24 flex-shrink-0 bg-black/20 rounded-xl p-1.5 flex items-center justify-center border border-white/20 group-hover:scale-105 transition-transform relative">
                            <img 
                                :src="getBeyImage(bey.photo)" 
                                :alt="bey.nombre"
                                class="w-full h-full object-contain"
                            >
                            <span 
                                v-if="bey.color" 
                                class="absolute -top-1 -right-1 w-4 h-4 rounded-full border border-white shadow-sm"
                                :style="{ backgroundColor: bey.color }"
                                :title="`Color: ${bey.color}`"
                            ></span>
                        </div>

                        <div class="flex flex-col items-start gap-1 flex-1 min-w-0">
                            <h3 class="text-lg font-extrabold text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors truncate w-full">
                                {{ bey.nombre }}
                            </h3>
                            <span v-if="bey.season" class="text-xs text-amber-600 dark:text-amber-400 font-semibold truncate w-full">
                                {{ bey.season }}
                            </span>
                            <span class="inline-flex items-center gap-1 px-2.5 py-0.5 bg-amber-500/15 text-amber-600 dark:text-amber-400 rounded-full text-[11px] font-semibold mt-1">
                                ⚡ Ver Beyblade →
                            </span>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit Character Modal -->
    <ModalEditarPersonajeComponent
        v-if="mostrarModalEditar && personaje"
        :personaje-id="personaje.id"
        @cerrar="mostrarModalEditar = false"
        @actualizado="cargarPersonaje"
    />

    <!-- Delete Character Confirmation Modal -->
    <ModalEliminarComponent
        v-if="mostrarModalEliminar && personaje"
        :texto="`¿Deseas eliminar al personaje '${personaje.nombre}'?`"
        texto-boton="Eliminar"
        texto-boton2="Cancelar"
        color="#E63946"
        @cancelar="mostrarModalEliminar = false"
        @eliminar="eliminarPersonaje"
    />

    <!-- Suggestion Modal for Normal Users -->
    <ModalSugerirComponent 
        v-if="mostrarModalSugerir" 
        tipo="personaje" 
        @cerrar="mostrarModalSugerir = false" 
    />
</template>


<style scoped>
</style>


