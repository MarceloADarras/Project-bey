<script setup>
import { ref, onMounted } from 'vue';
import api from '../src/main';

const props = defineProps({
    beyId: {
        type: [Number, String],
        required: true
    }
});

const emit = defineEmits(['cerrar', 'actualizado']);

const cargando = ref(true);
const guardando = ref(false);

const nombre = ref('');
const descripcion = ref('');
const fusion_wheel = ref('');
const clear_wheel = ref('');
const track = ref('');
const tip = ref('');
const tipe = ref('');
const color = ref('');
const season = ref('');
const sistema = ref('');
const fotoActual = ref('');
const nuevaImagen = ref(null);

const fusionWheels = ref([]);
const clearWheels = ref([]);
const tracks = ref([]);
const tips = ref([]);
const tipes = ref([]);

const errorMsg = ref('');

const cargarDatosBey = async () => {
    try {
        cargando.value = true;
        
        // Load Beyblade data and options in parallel
        const [resBey, resFus, resCle, resTra, resTip, resTipe] = await Promise.all([
            api.get(`cargar/bey/${props.beyId}`),
            api.get("cargar/fusion"),
            api.get("cargar/clear"),
            api.get("cargar/track"),
            api.get("cargar/tip"),
            api.get("cargar/tipe")
        ]);

        fusionWheels.value = resFus.data || [];
        clearWheels.value = resCle.data || [];
        tracks.value = resTra.data || [];
        tips.value = resTip.data || [];
        tipes.value = resTipe.data || [];

        const bey = resBey.data;
        nombre.value = bey.nombre || '';
        descripcion.value = bey.descripcion || '';
        fusion_wheel.value = bey.fusion_id || '';
        clear_wheel.value = bey.clear_id || '';
        track.value = bey.track_id || '';
        tip.value = bey.tip_id || '';
        tipe.value = bey.tipe_id || '';
        color.value = bey.color || '';
        season.value = bey.season || '';
        sistema.value = bey.sistem || '';
        fotoActual.value = bey.photo || '';

    } catch (error) {
        console.error('Error al cargar datos del Beyblade:', error);
        errorMsg.value = 'Error al obtener información del Beyblade.';
    } finally {
        cargando.value = false;
    }
};

const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        nuevaImagen.value = file;
    }
};

const guardarCambios = async () => {
    if (!nombre.value.trim()) {
        errorMsg.value = 'El nombre es obligatorio.';
        return;
    }

    try {
        guardando.value = true;
        errorMsg.value = '';

        const formData = new FormData();
        formData.append('nombre', nombre.value);
        formData.append('descripcion', descripcion.value);
        if (fusion_wheel.value) formData.append('fusion', fusion_wheel.value);
        if (clear_wheel.value) formData.append('clear', clear_wheel.value);
        if (track.value) formData.append('track', track.value);
        if (tip.value) formData.append('tip', tip.value);
        if (tipe.value) formData.append('tipe', tipe.value);
        if (color.value) formData.append('color', color.value);
        if (season.value) formData.append('season', season.value);
        if (sistema.value) formData.append('sistem', sistema.value);
        if (nuevaImagen.value) {
            formData.append('image', nuevaImagen.value);
        }

        await api.post(`editar/bey/${props.beyId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        emit('actualizado');
        emit('cerrar');
    } catch (error) {
        console.error('Error al actualizar Beyblade:', error);
        errorMsg.value = error.response?.data?.error || 'Error al guardar los cambios.';
    } finally {
        guardando.value = false;
    }
};

onMounted(() => {
    cargarDatosBey();
});
</script>

<template>
    <div class="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center p-4 z-50 overflow-y-auto">
        <div class="glass-card bg-slate-900/95 border border-slate-700/80 rounded-3xl p-6 sm:p-8 max-w-2xl w-full text-slate-100 shadow-2xl space-y-6 my-8">
            <!-- Modal Header -->
            <div class="flex items-center justify-between border-b border-slate-700 pb-4">
                <div class="flex items-center gap-2">
                    <span class="text-2xl">🌀</span>
                    <h2 class="font-extrabold text-xl">Editar Beyblade</h2>
                </div>
                <button 
                    type="button" 
                    @click="emit('cerrar')" 
                    class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                    ✕
                </button>
            </div>

            <!-- Loading -->
            <div v-if="cargando" class="text-center py-12 space-y-3">
                <div class="text-4xl animate-spin">🌀</div>
                <p class="text-xs font-semibold text-slate-400">Cargando información del Beyblade...</p>
            </div>

            <!-- Content Form -->
            <form v-else @submit.prevent="guardarCambios" class="space-y-5">
                <div v-if="errorMsg" class="p-3 bg-red-500/20 border border-red-500/40 text-red-300 rounded-xl text-xs font-semibold flex items-center gap-2">
                    <span>⚠️</span> {{ errorMsg }}
                </div>

                <!-- Nombre y Descripción -->
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Nombre *</label>
                        <input 
                            type="text" 
                            v-model="nombre" 
                            required
                            placeholder="Nombre del Beyblade" 
                            class="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                        >
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Descripción</label>
                        <textarea 
                            v-model="descripcion" 
                            rows="3"
                            placeholder="Descripción del Beyblade..." 
                            class="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                        ></textarea>
                    </div>
                </div>

                <!-- Piezas & Componentes -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Fusion Wheel</label>
                        <select v-model="fusion_wheel" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Rueda de Fusión</option>
                            <option v-for="f in fusionWheels" :key="f.id" :value="f.id">{{ f.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Clear Wheel</label>
                        <select v-model="clear_wheel" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Aro de Energía</option>
                            <option v-for="c in clearWheels" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Spin Track</label>
                        <select v-model="track" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Eje de Rotación</option>
                            <option v-for="t in tracks" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Tip</label>
                        <select v-model="tip" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Punta</option>
                            <option v-for="t in tips" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Tipo</label>
                        <select v-model="tipe" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Tipo</option>
                            <option v-for="t in tipes" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Temporada</label>
                        <select v-model="season" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Temporada</option>
                            <option value="Metal Fusion">Metal Fusion</option>
                            <option value="Metal Masters">Metal Masters</option>
                            <option value="Metal Fury">Metal Fury</option>
                        </select>
                    </div>
                </div>

                <!-- Sistema, Color e Imagen -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Sistema</label>
                        <select v-model="sistema" class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none">
                            <option value="">Seleccionar Sistema</option>
                            <option value="Pre-Hybrid">Sistema Pre-Híbrido</option>
                            <option value="Hybrid">Sistema Híbrido</option>
                            <option value="4D">Sistema 4D</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Color Predominante</label>
                        <input 
                            type="text" 
                            v-model="color" 
                            placeholder="#FF6B35 o nombre de color" 
                            class="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none"
                        >
                    </div>
                </div>

                <!-- Imagen Actual & Nueva Imagen -->
                <div class="space-y-2 pt-1">
                    <label class="block text-xs font-bold text-slate-300">Foto / Imagen del Beyblade</label>
                    <div class="flex items-center gap-4 bg-slate-800/80 p-3 rounded-2xl border border-slate-700">
                        <div v-if="fotoActual" class="w-16 h-16 rounded-xl bg-black/40 p-1 flex items-center justify-center flex-shrink-0 border border-white/20">
                            <img :src="fotoActual.startsWith('http') ? fotoActual : `https://project-bey-production.up.railway.app${fotoActual}`" alt="Preview" class="w-full h-full object-contain">
                        </div>
                        <div class="flex-1">
                            <input 
                                type="file" 
                                @change="handleImageChange" 
                                accept="image/*" 
                                class="text-xs text-slate-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-amber-500 file:text-white hover:file:bg-amber-600 cursor-pointer"
                            >
                            <p class="text-[10px] text-slate-400 mt-1">Selecciona una imagen solo si deseas cambiar la actual (se subirá a Cloudinary).</p>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-700">
                    <button 
                        type="button" 
                        @click="emit('cerrar')" 
                        class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-bold transition-colors"
                    >
                        Cancelar
                    </button>
                    <button 
                        type="submit" 
                        :disabled="guardando"
                        class="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                    >
                        <span v-if="guardando" class="animate-spin">🌀</span>
                        <span>{{ guardando ? 'Guardando...' : 'Guardar Cambios' }}</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
</style>
