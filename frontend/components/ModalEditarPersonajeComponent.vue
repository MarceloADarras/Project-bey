<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseButton from './BaseButton.vue';
import api from '../src/main';

const props = defineProps({
    personajeId: { type: [Number, String], required: true }
});

const emit = defineEmits(['cerrar', 'actualizado']);

const nombre = ref('');
const altura = ref('');
const peso = ref('');
const personalidad = ref('');
const historia = ref('');
const fotoActual = ref(null);
const nuevaFoto = ref(null);
const selectedBeyblades = ref([]);
const selectDropdownValue = ref('');

const beyblades = ref([]);
const cargando = ref(true);
const guardando = ref(false);
const errorMsg = ref('');
const busquedaBey = ref('');
const mostrarCatalogo = ref(false);

const cargarDatos = async () => {
    try {
        cargando.value = true;
        // Fetch Beyblades catalog
        const resBeys = await api.get('cargar/beyblade');
        beyblades.value = resBeys.data || [];

        // Fetch Character details
        const resPersonaje = await api.get(`cargar/personaje/${props.personajeId}`);
        const p = resPersonaje.data;

        nombre.value = p.nombre || '';
        altura.value = p.altura || '';
        peso.value = p.peso || '';
        personalidad.value = p.personalidad || '';
        historia.value = p.historia || '';
        fotoActual.value = p.foto || null;

        if (p.beyblades && p.beyblades.length > 0) {
            selectedBeyblades.value = p.beyblades.map(b => b.id);
        } else if (p.beyblade) {
            selectedBeyblades.value = [p.beyblade.id];
        } else {
            selectedBeyblades.value = [];
        }
    } catch (error) {
        console.error('Error al cargar datos para edición:', error);
        errorMsg.value = 'No se pudo cargar la información del personaje.';
    } finally {
        cargando.value = false;
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

const handleFotoChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
        nuevaFoto.value = files[0];
    }
};

const getBeyImage = (photoPath) => {
    if (!photoPath) return '/img/image.png';
    if (photoPath.startsWith('http')) return photoPath;
    return `https://project-bey-production.up.railway.app${photoPath}`;
};

const guardarCambios = async () => {
    errorMsg.value = '';
    if (!nombre.value.trim()) {
        errorMsg.value = 'El nombre del personaje es obligatorio.';
        return;
    }

    try {
        guardando.value = true;
        const formData = new FormData();
        formData.append('nombre', nombre.value);
        formData.append('altura', altura.value);
        formData.append('peso', peso.value);
        formData.append('personalidad', personalidad.value);
        formData.append('historia', historia.value);

        if (selectedBeyblades.value.length === 0) {
            formData.append('beyblades', '');
        } else {
            selectedBeyblades.value.forEach(bId => {
                formData.append('beyblades', bId);
            });
        }

        if (nuevaFoto.value) {
            formData.append('foto', nuevaFoto.value);
        }

        await api.post(`editar/personaje/${props.personajeId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        emit('actualizado');
        emit('cerrar');
    } catch (error) {
        console.error('Error al editar personaje:', error);
        errorMsg.value = error.response?.data?.error || 'Ocurrió un error al guardar los cambios.';
    } finally {
        guardando.value = false;
    }
};

onMounted(() => {
    cargarDatos();
});
</script>

<template>
    <div class="fixed inset-0 w-screen h-screen bg-black/60 backdrop-blur-sm flex items-center justify-center z-[9999] p-4 overflow-y-auto">
        <div class="glass-card flex flex-col max-w-2xl w-full p-6 sm:p-8 rounded-3xl gap-5 shadow-2xl text-slate-900 dark:text-slate-100 max-h-[90vh] overflow-y-auto border border-white/20">
            <!-- Header -->
            <div class="flex justify-between items-center border-b border-slate-200 dark:border-slate-700/60 pb-3">
                <h2 class="text-2xl font-extrabold flex items-center gap-2 text-slate-900 dark:text-slate-100">
                    <span>✏️</span> Editar Personaje
                </h2>
                <button 
                    type="button" 
                    @click="emit('cerrar')" 
                    class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 flex items-center justify-center font-bold text-sm transition-colors"
                >
                    ✕
                </button>
            </div>

            <!-- Loading State -->
            <div v-if="cargando" class="text-center py-12 text-slate-600 dark:text-slate-300">
                <div class="text-3xl animate-spin mb-2">🌀</div>
                <p class="font-semibold text-sm">Cargando datos del personaje...</p>
            </div>

            <!-- Form -->
            <form v-else @submit.prevent="guardarCambios" class="space-y-4">
                <div v-if="errorMsg" class="p-3 bg-red-500/10 border border-red-500/40 rounded-xl text-red-600 dark:text-red-400 text-xs font-semibold text-center">
                    {{ errorMsg }}
                </div>

                <!-- Nombre -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre del Personaje *</label>
                    <input 
                        type="text" 
                        v-model="nombre" 
                        required 
                        class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                    >
                </div>

                <!-- Altura & Peso -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Altura</label>
                        <input 
                            type="text" 
                            v-model="altura" 
                            placeholder="Ej: 1.68 m" 
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                        >
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Peso</label>
                        <input 
                            type="text" 
                            v-model="peso" 
                            placeholder="Ej: 58 kg" 
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                        >
                    </div>
                </div>

                <!-- Beyblades Asignados -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center">
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                            <span>⚡ Beyblades Asignados</span>
                            <span class="px-2 py-0.5 bg-amber-500/20 text-amber-600 dark:text-amber-400 rounded-full text-[10px] font-bold">
                                {{ selectedBeyblades.length }} seleccionados
                            </span>
                        </label>
                        <button 
                            type="button" 
                            @click="mostrarCatalogo = !mostrarCatalogo"
                            class="text-[11px] font-semibold text-amber-500 hover:text-amber-600 hover:underline flex items-center gap-1 cursor-pointer"
                        >
                            {{ mostrarCatalogo ? '✖ Ocultar Catálogo' : '🔍 Catálogo Visual' }}
                        </button>
                    </div>

                    <!-- Dropdown Select & Search -->
                    <div class="space-y-2">
                        <select 
                            v-model="selectDropdownValue" 
                            @change="handleDropdownSelect"
                            class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                        >
                            <option value="">+ Agregar Beyblade...</option>
                            <option v-for="b in beybladesFiltrados" :key="b.id" :value="b.id">
                                {{ selectedBeyblades.includes(b.id) ? '✓ ' : '' }}{{ b.nombre }} {{ b.season ? `(${b.season})` : '' }}
                            </option>
                        </select>
                    </div>

                    <!-- Visual Grid Catalog -->
                    <div v-if="mostrarCatalogo" class="p-3 bg-slate-900/10 dark:bg-slate-800/50 border border-amber-500/30 rounded-2xl space-y-2 max-h-48 overflow-y-auto">
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
                                    class="w-10 h-10 object-contain bg-black/10 rounded-lg p-1"
                                >
                                <span class="text-xs font-bold text-slate-900 dark:text-slate-100 line-clamp-1">{{ b.nombre }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Selected Beyblades Badges -->
                    <div v-if="selectedBeyObjects.length > 0" class="flex flex-wrap gap-2 pt-1">
                        <div 
                            v-for="b in selectedBeyObjects" 
                            :key="b.id"
                            class="px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-xl text-xs font-semibold flex items-center gap-2"
                        >
                            <span>{{ b.nombre }}</span>
                            <button type="button" @click="desasignarBeyblade(b.id)" class="hover:text-red-500 font-bold">✕</button>
                        </div>
                    </div>
                </div>

                <!-- Personalidad -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Personalidad</label>
                    <textarea 
                        v-model="personalidad" 
                        rows="2" 
                        class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 p-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                    ></textarea>
                </div>

                <!-- Historia -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Historia</label>
                    <textarea 
                        v-model="historia" 
                        rows="3" 
                        class="w-full bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 p-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner text-sm"
                    ></textarea>
                </div>

                <!-- Foto actual & Nueva Foto -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Foto del Personaje</label>
                    <div class="flex items-center gap-4 bg-white/90 dark:bg-slate-800 p-3 rounded-xl border border-slate-300 dark:border-slate-700">
                        <img 
                            v-if="fotoActual" 
                            :src="fotoActual.startsWith('http') ? fotoActual : `https://project-bey-production.up.railway.app${fotoActual}`" 
                            class="w-12 h-12 object-cover rounded-lg border"
                        >
                        <input 
                            type="file" 
                            @change="handleFotoChange" 
                            accept="image/*" 
                            class="text-xs text-slate-700 dark:text-slate-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-amber-500 file:text-white hover:file:bg-amber-600 cursor-pointer"
                        >
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-end gap-3 pt-4 border-t border-slate-200 dark:border-slate-700/60">
                    <BaseButton color="#64748B" hoverColor="#475569" type="button" @click="emit('cerrar')">Cancelar</BaseButton>
                    <BaseButton color="#FF6B35" hoverColor="#E63946" type="submit" :disabled="guardando">
                        {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
                    </BaseButton>
                </div>
            </form>
        </div>
    </div>
</template>
