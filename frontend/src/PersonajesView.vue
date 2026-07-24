<script setup>
import { ref, computed, onMounted } from 'vue';
import Header from '../components/HeaderComponent.vue';
import CardPersonaje from '../components/CardPersonaje.vue';
import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
import ModalEditarPersonajeComponent from '../components/ModalEditarPersonajeComponent.vue';
import ModalSugerirComponent from '../components/ModalSugerirComponent.vue';
import api from './main';

const personajes = ref([]);
const cargando = ref(true);

const personajeAEditarId = ref(null);
const personajeAEliminar = ref(null);
const eliminando = ref(false);
const mostrarModalSugerir = ref(false);

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;
const esAdmin = computed(() => localUser?.is_staff || localUser?.is_superuser || false);

const cargarPersonajes = async () => {
    try {
        cargando.value = true;
        const res = await api.get('cargar/personajes');
        personajes.value = res.data;
        console.log('Personajes cargados:', personajes.value);
    } catch (error) {
        console.error('Error al cargar personajes:', error);
    } finally {
        cargando.value = false;
    }
};

const abrirEditar = (id) => {
    personajeAEditarId.value = id;
};

const abrirEliminar = (personaje) => {
    personajeAEliminar.value = personaje;
};

const confirmarEliminar = async () => {
    if (!personajeAEliminar.value) return;
    try {
        eliminando.value = true;
        await api.post(`eliminar/personaje/${personajeAEliminar.value.id}`);
        personajeAEliminar.value = null;
        await cargarPersonajes();
    } catch (error) {
        console.error('Error al eliminar personaje:', error);
    } finally {
        eliminando.value = false;
    }
};

onMounted(() => {
    cargarPersonajes();
});
</script>

<template>
    <Header></Header>

    <div class="min-h-[calc(100vh-64px)] p-6 max-w-7xl mx-auto flex flex-col items-center">
        <!-- View Header Title -->
        <div class="glass-card text-center px-8 py-5 rounded-2xl mb-8 w-full max-w-3xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="text-center" :class="{ 'sm:text-left': personajes.length > 0, 'w-full': personajes.length === 0 }">
                <h1 class="font-bold text-3xl text-slate-900 dark:text-slate-100">Bladers & Personajes</h1>
                <p class="text-xs text-slate-600 dark:text-slate-300 mt-1">Conoce a los personajes legendarios de BeyStory y sus Beyblades asociados.</p>
            </div>
            
            <template v-if="personajes.length > 0">
                <router-link 
                    v-if="esAdmin"
                    to="/create/personaje" 
                    class="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all hover:scale-105 no-underline flex items-center gap-1.5 flex-shrink-0"
                >
                    <span>➕</span> Crear Personaje
                </router-link>
                <button 
                    v-else-if="localUser"
                    @click="mostrarModalSugerir = true"
                    class="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all hover:scale-105 flex items-center gap-1.5 flex-shrink-0 cursor-pointer"
                >
                    <span>💡</span> Sugerir Personaje
                </button>
            </template>
        </div>

        <!-- Loading State -->
        <div v-if="cargando" class="glass-card p-8 rounded-2xl text-center text-slate-600 dark:text-slate-300 max-w-md w-full my-12">
            <div class="text-3xl animate-spin mb-2">🌀</div>
            <p class="font-semibold text-sm">Cargando personajes...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="personajes.length === 0" class="glass-card p-10 rounded-3xl text-center max-w-md w-full my-8 space-y-5 flex flex-col items-center justify-center shadow-2xl">
            <span class="text-5xl">👥</span>
            <div class="space-y-1">
                <h2 class="font-extrabold text-2xl text-slate-900 dark:text-slate-100">No hay personajes registrados</h2>
                <p class="text-xs text-slate-600 dark:text-slate-300">Sé el primero en registrar a un blader legendario en la plataforma.</p>
            </div>
            <router-link 
                v-if="esAdmin"
                to="/create/personaje" 
                class="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-2xl text-sm font-extrabold shadow-xl transition-all hover:scale-105 no-underline flex items-center justify-center gap-2"
            >
                <span>➕</span> Crear Personaje
            </router-link>
            <button 
                v-else-if="localUser"
                @click="mostrarModalSugerir = true" 
                class="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-2xl text-sm font-extrabold shadow-xl transition-all hover:scale-105 flex items-center justify-center gap-2 cursor-pointer"
            >
                <span>💡</span> Sugerir Personaje
            </button>
        </div>



        <!-- Characters Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 w-full px-4 justify-items-center">
            <CardPersonaje 
                v-for="p in personajes" 
                :key="p.id"
                :id="p.id"
                :nombre="p.nombre"
                :altura="p.altura"
                :peso="p.peso"
                :personalidad="p.personalidad"
                :historia="p.historia"
                :foto="p.foto"
                :beyblades="p.beyblades"
                @editar="abrirEditar"
                @eliminar="abrirEliminar"
            />
        </div>
    </div>

    <!-- Edit Character Modal -->
    <ModalEditarPersonajeComponent
        v-if="personajeAEditarId"
        :personaje-id="personajeAEditarId"
        @cerrar="personajeAEditarId = null"
        @actualizado="cargarPersonajes"
    />

    <!-- Delete Character Confirmation Modal -->
    <ModalEliminarComponent
        v-if="personajeAEliminar"
        :texto="`¿Deseas eliminar al personaje '${personajeAEliminar.nombre}'?`"
        texto-boton="Eliminar"
        texto-boton2="Cancelar"
        color="#E63946"
        @cancelar="personajeAEliminar = null"
        @eliminar="confirmarEliminar"
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

