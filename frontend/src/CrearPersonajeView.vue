<script setup>
import { ref, computed, onMounted } from 'vue';
import Header from '../components/HeaderComponent.vue';
import BaseButton from '../components/BaseButton.vue';
import LoadingOverlay from '../components/LoadingOverlay.vue';
import api from './main';
import { useRouter } from 'vue-router';

const router = useRouter();

const nombre = ref('');
const altura = ref('');
const peso = ref('');
const personalidad = ref('');
const historia = ref('');
const selectedBeyblades = ref([]); // List of selected Beyblade IDs
const selectDropdownValue = ref('');
const foto = ref(null);

const beyblades = ref([]);
const cargandoBeys = ref(true);
const errorCargaBeys = ref(false);
const busquedaBey = ref('');
const mostrarCatalogo = ref(false);

const cargando = ref(false);
const mensajeCarga = ref('Guardando personaje...');
const errorMsg = ref('');

const cargarBeyblades = async () => {
    try {
        cargandoBeys.value = true;
        errorCargaBeys.value = false;
        const res = await api.get('cargar/beyblade');
        beyblades.value = res.data || [];
        console.log('Beyblades cargados para asignación:', beyblades.value);
    } catch (error) {
        console.error('Error al cargar Beyblades:', error);
        errorCargaBeys.value = true;
    } finally {
        cargandoBeys.value = false;
    }
};

const beybladesFiltrados = computed(() => {
    if (!busquedaBey.value.trim()) return beyblades.value;
    const q = busquedaBey.value.toLowerCase();
    return beyblades.value.filter(b => 
        (b.nombre && b.nombre.toLowerCase().includes(q)) || 
        (b.season && b.season.toLowerCase().includes(q))
    );
});

const selectedBeyObjects = computed(() => {
    return beyblades.value.filter(b => selectedBeyblades.value.includes(b.id));
});

const toggleBeySelection = (id) => {
    const numId = Number(id);
    if (!numId) return;
    const index = selectedBeyblades.value.indexOf(numId);
    if (index > -1) {
        selectedBeyblades.value.splice(index, 1);
    } else {
        selectedBeyblades.value.push(numId);
    }
};

const handleDropdownSelect = (e) => {
    const val = Number(e.target.value);
    if (val) {
        if (!selectedBeyblades.value.includes(val)) {
            selectedBeyblades.value.push(val);
        }
        selectDropdownValue.value = '';
    }
};

const desasignarBeyblade = (id) => {
    selectedBeyblades.value = selectedBeyblades.value.filter(bId => bId !== id);
};

const getBeyImage = (photoPath) => {
    if (!photoPath) return '/img/image.png';
    if (photoPath.startsWith('http')) return photoPath;
    return `https://project-bey-production.up.railway.app${photoPath}`;
};

const handleFotoChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
        foto.value = files[0];
    }
};

const crearPersonaje = async () => {
    errorMsg.value = '';
    
    if (!nombre.value.trim()) {
        errorMsg.value = 'El nombre del personaje es obligatorio.';
        return;
    }

    try {
        cargando.value = true;
        mensajeCarga.value = `Creando el personaje ${nombre.value}...`;

        const formData = new FormData();
        formData.append('nombre', nombre.value);
        formData.append('altura', altura.value);
        formData.append('peso', peso.value);
        formData.append('personalidad', personalidad.value);
        formData.append('historia', historia.value);
        
        selectedBeyblades.value.forEach(bId => {
            formData.append('beyblades', bId);
        });

        if (foto.value) {
            formData.append('foto', foto.value);
        }

        await api.post('crear/personaje', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        mensajeCarga.value = '¡Personaje creado exitosamente! Redirigiendo...';

        setTimeout(() => {
            cargando.value = false;
            router.push('/personajes');
        }, 1000);

    } catch (error) {
        cargando.value = false;
        console.error('Error al crear personaje:', error);
        errorMsg.value = error.response?.data?.error || 'Ocurrió un error al guardar el personaje.';
    }
};

onMounted(() => {
    cargarBeyblades();
});
</script>

<template>
    <Header></Header>
    <LoadingOverlay :cargando="cargando" :mensaje="mensajeCarga" />

    <div class="flex flex-col items-center justify-center p-6 max-w-3xl mx-auto min-h-[calc(100vh-64px)]">
        <form @submit.prevent="crearPersonaje" class="w-full">
            <div class="glass-card relative flex flex-col justify-center items-center p-8 rounded-3xl gap-6 w-full shadow-2xl text-slate-900 dark:text-slate-100">
                <div class="text-center">
                    <h1 class="font-extrabold text-3xl mb-1 text-slate-900 dark:text-slate-100">👤 Crear Personaje</h1>
                    <p class="text-xs text-slate-600 dark:text-slate-300">Completa la información para registrar a un nuevo blader y asignarle sus Beyblades.</p>
                </div>

                <div v-if="errorMsg" class="w-full p-3 bg-red-500/10 border border-red-500/40 rounded-xl text-red-600 dark:text-red-400 text-xs font-semibold text-center">
                    {{ errorMsg }}
                </div>

                <div class="w-full space-y-4">
                    <!-- Nombre -->
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre del Personaje *</label>
                        <input 
                            type="text" 
                            v-model="nombre" 
                            required 
                            placeholder="Ej: Gingka Hagane" 
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner"
                        >
                    </div>

                    <!-- Altura & Peso -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Altura</label>
                            <input 
                                type="text" 
                                v-model="altura" 
                                placeholder="Ej: 1.68 m" 
                                class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner"
                            >
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Peso</label>
                            <input 
                                type="text" 
                                v-model="peso" 
                                placeholder="Ej: 58 kg" 
                                class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner"
                            >
                        </div>
                    </div>

                    <!-- Beyblades Asignados (Multiple Selection) -->
                    <div class="space-y-2">
                        <div class="flex justify-between items-center">
                            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                                <span>⚡ Beyblades Asignados</span>
                                <span class="px-2 py-0.5 bg-amber-500/20 text-amber-600 dark:text-amber-400 rounded-full text-[10px] font-bold">
                                    {{ selectedBeyblades.length }} seleccionados
                                </span>
                            </label>
                            <div class="flex items-center gap-2">
                                <span v-if="cargandoBeys" class="text-[11px] text-amber-600 dark:text-amber-400 animate-pulse flex items-center gap-1">
                                    <span>🌀</span> Cargando beyblades...
                                </span>
                                <button 
                                    v-if="!cargandoBeys && beyblades.length > 0" 
                                    type="button" 
                                    @click="mostrarCatalogo = !mostrarCatalogo"
                                    class="text-[11px] font-semibold text-amber-500 hover:text-amber-600 hover:underline flex items-center gap-1 cursor-pointer"
                                >
                                    {{ mostrarCatalogo ? '✖ Ocultar Catálogo' : '🔍 Catálogo Visual' }}
                                </button>
                            </div>
                        </div>

                        <!-- Fallback / Error State -->
                        <div v-if="errorCargaBeys" class="p-3 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center justify-between text-xs text-red-600 dark:text-red-400">
                            <span>Error al cargar Beyblades desde el servidor.</span>
                            <button type="button" @click="cargarBeyblades" class="px-2 py-1 bg-red-500 text-white rounded-lg hover:bg-red-600 font-semibold transition-colors">
                                Reintentar
                            </button>
                        </div>

                        <!-- Main Dropdown Select & Search -->
                        <div v-else class="space-y-2">
                            <div class="flex gap-2">
                                <select 
                                    v-model="selectDropdownValue" 
                                    @change="handleDropdownSelect"
                                    :disabled="cargandoBeys"
                                    class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner disabled:opacity-60 transition-colors text-sm"
                                >
                                    <option value="">{{ cargandoBeys ? 'Cargando lista de beyblades...' : (beyblades.length === 0 ? 'No hay beyblades disponibles' : '+ Agregar Beyblade a la lista...') }}</option>
                                    <option v-for="b in beybladesFiltrados" :key="b.id" :value="b.id">
                                        {{ selectedBeyblades.includes(b.id) ? '✓ ' : '' }}{{ b.nombre }} {{ b.season ? `(${b.season})` : '' }}
                                    </option>
                                </select>
                            </div>

                            <!-- Search Filter Input -->
                            <div v-if="!cargandoBeys && beyblades.length > 5" class="relative">
                                <input 
                                    type="text" 
                                    v-model="busquedaBey" 
                                    placeholder="🔍 Filtrar beyblades por nombre o temporada..." 
                                    class="w-full bg-white/70 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/70 text-slate-800 dark:text-slate-200 px-3 py-1.5 rounded-lg text-xs focus:outline-none focus:border-amber-500"
                                >
                            </div>
                        </div>

                        <!-- Visual Grid Catalog Drawer / Modal -->
                        <div v-if="mostrarCatalogo && !cargandoBeys" class="p-4 bg-slate-900/10 dark:bg-slate-800/50 border border-amber-500/30 rounded-2xl space-y-3 max-h-64 overflow-y-auto">
                            <div class="flex justify-between items-center">
                                <span class="text-xs font-bold text-amber-600 dark:text-amber-400">Haz clic en los Beyblades para agregarlos o quitarlos:</span>
                                <span class="text-[10px] text-slate-500 dark:text-slate-400">{{ beybladesFiltrados.length }} disponibles</span>
                            </div>
                            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                <div 
                                    v-for="b in beybladesFiltrados" 
                                    :key="b.id"
                                    @click="toggleBeySelection(b.id)"
                                    :class="[
                                        'p-2 rounded-xl border flex flex-col items-center gap-1 cursor-pointer transition-all hover:scale-105 text-center relative',
                                        selectedBeyblades.includes(b.id) ? 'bg-amber-500/25 border-amber-500 ring-2 ring-amber-500/50' : 'bg-white/80 dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-amber-400'
                                    ]"
                                >
                                    <span v-if="selectedBeyblades.includes(b.id)" class="absolute top-1 right-1 bg-amber-500 text-white w-4 h-4 rounded-full text-[10px] font-bold flex items-center justify-center shadow">✓</span>
                                    <img 
                                        :src="getBeyImage(b.photo)" 
                                        :alt="b.nombre" 
                                        class="w-12 h-12 object-contain bg-black/10 rounded-lg p-1"
                                    >
                                    <span class="text-xs font-bold text-slate-900 dark:text-slate-100 line-clamp-1">{{ b.nombre }}</span>
                                    <span class="text-[10px] text-amber-600 dark:text-amber-400 font-medium">{{ b.season || 'Bey' }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Live Selected Beyblades Preview Cards Grid -->
                        <div v-if="selectedBeyObjects.length > 0" class="space-y-2 mt-3">
                            <h4 class="text-xs font-bold text-slate-700 dark:text-slate-300">Beyblades asignados a este personaje:</h4>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                <div 
                                    v-for="b in selectedBeyObjects" 
                                    :key="b.id"
                                    class="p-3 bg-gradient-to-r from-amber-500/15 to-orange-500/15 border border-amber-500/40 rounded-2xl flex items-center gap-3 transition-all shadow-sm"
                                >
                                    <div class="relative w-12 h-12 bg-black/20 rounded-xl p-1 flex items-center justify-center border border-white/20 flex-shrink-0">
                                        <img 
                                            :src="getBeyImage(b.photo)" 
                                            :alt="b.nombre"
                                            class="w-full h-full object-contain"
                                        >
                                        <span 
                                            v-if="b.color" 
                                            class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full border border-white shadow-sm"
                                            :style="{ backgroundColor: b.color }"
                                            :title="`Color: ${b.color}`"
                                        ></span>
                                    </div>

                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-extrabold text-xs text-slate-900 dark:text-slate-100 truncate">{{ b.nombre }}</h4>
                                        <p class="text-[11px] text-amber-600 dark:text-amber-400 font-medium truncate">
                                            {{ b.season || 'Beyblade' }}
                                        </p>
                                    </div>

                                    <button 
                                        type="button" 
                                        @click="desasignarBeyblade(b.id)" 
                                        class="px-2.5 py-1 bg-red-500/10 hover:bg-red-500/25 border border-red-500/30 text-red-600 dark:text-red-400 rounded-lg text-xs font-semibold transition-colors cursor-pointer"
                                        title="Quitar Beyblade"
                                    >
                                        ✕
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Personalidad -->
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Personalidad</label>
                        <textarea 
                            v-model="personalidad" 
                            rows="3" 
                            placeholder="Describe los rasgos de personalidad del personaje..." 
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner"
                        ></textarea>
                    </div>

                    <!-- Historia -->
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Historia</label>
                        <textarea 
                            v-model="historia" 
                            rows="4" 
                            placeholder="Escribe la historia o biografía del personaje..." 
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner"
                        ></textarea>
                    </div>

                    <!-- Foto del Personaje -->
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Foto del Personaje</label>
                        <div class="border border-slate-300 dark:border-slate-700 bg-white/90 dark:bg-slate-800 p-4 rounded-xl shadow-inner">
                            <input 
                                type="file" 
                                @change="handleFotoChange" 
                                accept="image/*" 
                                class="text-xs text-slate-700 dark:text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-amber-500 file:text-white hover:file:bg-amber-600 cursor-pointer"
                            >
                        </div>
                    </div>
                </div>

                <div class="mt-4">
                    <BaseButton color="#FF6B35" hoverColor="#E63946" @click="crearPersonaje()">Crear Personaje</BaseButton>
                </div>
            </div>
        </form>
    </div>
</template>

<style scoped>
</style>

