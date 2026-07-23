<script setup>
import { ref } from 'vue';
import api from '../src/main';

const props = defineProps({
    tipo: {
        type: String,
        default: 'beyblade' // 'beyblade' o 'personaje'
    }
});

const emit = defineEmits(['cerrar', 'enviado']);

const nombre = ref('');
const descripcion = ref('');
const opcional = ref('');

const enviando = ref(false);
const mensaje = ref({ tipo: '', texto: '' });

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;

const enviarSugerencia = async () => {
    if (!nombre.value.trim()) {
        mensaje.value = { tipo: 'error', texto: 'El nombre es obligatorio.' };
        return;
    }

    try {
        enviando.value = true;
        mensaje.value = { tipo: '', texto: '' };

        const payload = {
            tipo: props.tipo,
            nombre: nombre.value,
            descripcion: descripcion.value,
            opcional: opcional.value,
            user_id: localUser?.id
        };

        const res = await api.post('crear/reporte', payload);
        mensaje.value = { tipo: 'exito', texto: res.data.success || 'Sugerencia enviada correctamente.' };
        
        setTimeout(() => {
            emit('enviado');
            emit('cerrar');
        }, 1200);
    } catch (error) {
        console.error('Error al enviar sugerencia:', error);
        mensaje.value = { tipo: 'error', texto: error.response?.data?.error || 'Error al enviar la sugerencia.' };
    } finally {
        enviando.value = false;
    }
};
</script>

<template>
    <div class="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center p-4 z-50 overflow-y-auto">
        <div class="glass-card bg-slate-900/95 border border-slate-700/80 rounded-3xl p-6 sm:p-8 max-w-lg w-full text-slate-100 shadow-2xl space-y-6 my-8">
            <!-- Header -->
            <div class="flex items-center justify-between border-b border-slate-700 pb-4">
                <div class="flex items-center gap-2">
                    <span class="text-2xl">{{ tipo === 'personaje' ? '👤' : '🌀' }}</span>
                    <div>
                        <h2 class="font-extrabold text-xl">Sugerir {{ tipo === 'personaje' ? 'Personaje' : 'Beyblade' }}</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Envía una solicitud al equipo de administración.</p>
                    </div>
                </div>
                <button 
                    type="button" 
                    @click="emit('cerrar')" 
                    class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                    ✕
                </button>
            </div>

            <!-- Feedback -->
            <div 
                v-if="mensaje.texto" 
                class="p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2"
                :class="mensaje.tipo === 'exito' ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-300' : 'bg-red-500/20 border border-red-500/40 text-red-300'"
            >
                <span>{{ mensaje.tipo === 'exito' ? '✅' : '⚠️' }}</span>
                <span>{{ mensaje.texto }}</span>
            </div>

            <!-- Form -->
            <form @submit.prevent="enviarSugerencia" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-300 mb-1">Nombre *</label>
                    <input 
                        type="text" 
                        v-model="nombre" 
                        required
                        :placeholder="tipo === 'personaje' ? 'Nombre del personaje / Blader' : 'Nombre del Beyblade'" 
                        class="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                    >
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-300 mb-1">Descripción</label>
                    <textarea 
                        v-model="descripcion" 
                        rows="3"
                        placeholder="Detalles del elemento a sugerir..." 
                        class="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                    ></textarea>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-300 mb-1">Información Adicional (Opcional)</label>
                    <textarea 
                        v-model="opcional" 
                        rows="2"
                        :placeholder="tipo === 'personaje' ? 'Ej: Beyblades asociados, apariciones en temporadas...' : 'Ej: Piezas principales (Fusion, Clear, Track, Tip), temporada...'" 
                        class="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                    ></textarea>
                </div>

                <!-- Warning Notice with asterisk -->
                <div class="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-[11px] text-amber-400 font-semibold leading-relaxed">
                    <span>* Los reportes o sugerencias rechazados se eliminarán automáticamente de la base de datos tras 30 días.</span>
                </div>

                <!-- Action Buttons -->
                <div class="flex items-center justify-end gap-3 pt-2">
                    <button 
                        type="button" 
                        @click="emit('cerrar')" 
                        class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-bold transition-colors"
                    >
                        Cancelar
                    </button>
                    <button 
                        type="submit" 
                        :disabled="enviando"
                        class="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                    >
                        <span v-if="enviando" class="animate-spin">🌀</span>
                        <span>{{ enviando ? 'Enviando...' : '💡 Enviar Sugerencia' }}</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
</style>
