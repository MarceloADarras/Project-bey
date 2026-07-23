<script setup>
import { computed } from 'vue';

const props = defineProps({
    id: { type: [Number, String], required: true },
    nombre: { type: String, required: true },
    altura: String,
    peso: String,
    personalidad: String,
    historia: String,
    foto: String,
    beybladeNombre: String,
    beyblades: Array
});

const emit = defineEmits(['editar', 'eliminar']);

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;
const esAdmin = computed(() => localUser?.is_staff || localUser?.is_superuser || false);

const displayBeybladesText = computed(() => {
    if (props.beyblades && props.beyblades.length > 0) {
        return props.beyblades.map(b => b.nombre).join(', ');
    }
    return props.beybladeNombre || null;
});
</script>

<template>
    <div class="glass-card flex flex-col items-center justify-between p-5 rounded-2xl transition-all duration-300 hover:-translate-y-1.5 hover:border-amber-500 shadow-xl overflow-hidden cursor-pointer group text-slate-900 dark:text-slate-100 w-full max-w-xs relative">
        <!-- Top Action Buttons (Edit / Delete) - ADMIN ONLY -->
        <div v-if="esAdmin" class="absolute top-3 right-3 flex items-center gap-1.5 z-20">
            <button 
                type="button" 
                @click.stop.prevent="emit('editar', id)" 
                class="w-7 h-7 bg-white/80 dark:bg-slate-800/80 hover:bg-amber-500 text-slate-700 dark:text-slate-200 hover:text-white rounded-lg flex items-center justify-center transition-all text-xs border border-slate-300 dark:border-slate-600 hover:border-amber-500 shadow-sm"
                title="Editar personaje"
            >
                ✏️
            </button>
            <button 
                type="button" 
                @click.stop.prevent="emit('eliminar', { id, nombre })" 
                class="w-7 h-7 bg-white/80 dark:bg-slate-800/80 hover:bg-red-500 text-slate-700 dark:text-slate-200 hover:text-white rounded-lg flex items-center justify-center transition-all text-xs border border-slate-300 dark:border-slate-600 hover:border-red-500 shadow-sm"
                title="Eliminar personaje"
            >
                🗑️
            </button>
        </div>


        <router-link :to="{ name: 'VerPersonaje', params: { id: id } }" class="no-underline text-inherit w-full flex flex-col items-center gap-4">
            <!-- Character Image / Avatar Container -->
            <div class="relative w-36 h-36 rounded-2xl overflow-hidden border border-white/40 dark:border-slate-700 bg-black/10 flex items-center justify-center shadow-inner group-hover:scale-105 transition-transform duration-300">
                <img 
                    v-if="foto" 
                    :src="foto.startsWith('http') ? foto : `https://project-bey-production.up.railway.app${foto}`" 
                    :alt="nombre"
                    class="w-full h-full object-cover"
                >
                <span v-else class="text-5xl">👤</span>
            </div>

            <!-- Main Info -->
            <div class="text-center w-full space-y-2">
                <h3 class="font-bold text-xl text-slate-900 dark:text-slate-100 group-hover:text-amber-500 transition-colors line-clamp-1">
                    {{ nombre }}
                </h3>

                <!-- Associated Beyblade Badge -->
                <div v-if="displayBeybladesText" class="inline-flex items-center gap-1 px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-semibold max-w-full">
                    <span class="flex-shrink-0">⚡</span> 
                    <span class="truncate">{{ displayBeybladesText }}</span>
                </div>
                <div v-else class="inline-flex items-center gap-1 px-3 py-1 bg-slate-500/15 border border-slate-500/30 text-slate-500 dark:text-slate-400 rounded-full text-xs">
                    Sin Beyblade
                </div>

                <!-- Stats summary -->
                <div class="flex items-center justify-center gap-3 text-xs text-slate-600 dark:text-slate-300 pt-1">
                    <span v-if="altura" class="px-2 py-0.5 bg-white/50 dark:bg-slate-800/80 rounded-md border border-slate-200 dark:border-slate-700">📏 {{ altura }}</span>
                    <span v-if="peso" class="px-2 py-0.5 bg-white/50 dark:bg-slate-800/80 rounded-md border border-slate-200 dark:border-slate-700">⚖️ {{ peso }}</span>
                </div>
            </div>
        </router-link>
    </div>
</template>

<style scoped>
</style>

