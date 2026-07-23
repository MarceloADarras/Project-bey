<script setup>
import { ref, computed, onMounted } from 'vue';
import Header from '../components/HeaderComponent.vue';
import api from './main';

const reportes = ref([]);
const cargando = ref(true);
const filtroEstado = ref('todos'); // 'todos', 'pendiente', 'aceptado', 'rechazado'

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;
const esAdmin = computed(() => localUser?.is_staff || localUser?.is_superuser || false);

const cargarReportes = async () => {
    try {
        cargando.value = true;
        let endpoint = 'cargar/reportes';
        if (localUser?.id) {
            endpoint = `cargar/reportes?user_id=${localUser.id}`;
        }
        const res = await api.get(endpoint);
        reportes.value = res.data || [];
    } catch (error) {
        console.error('Error al cargar reportes:', error);
    } finally {
        cargando.value = false;
    }
};

const reportesFiltrados = computed(() => {
    if (filtroEstado.value === 'todos') {
        return reportes.value;
    }
    return reportes.value.filter(r => r.estado === filtroEstado.value);
});

const responderReporte = async (id, nuevoEstado) => {
    try {
        await api.post(`responder/reporte/${id}`, {
            estado: nuevoEstado,
            user_id: localUser?.id
        });
        await cargarReportes();
    } catch (error) {
        console.error('Error al responder reporte:', error);
        alert(error.response?.data?.error || 'Error al procesar el reporte.');
    }
};

onMounted(() => {
    cargarReportes();
});
</script>

<template>
    <Header></Header>

    <div class="min-h-[calc(100vh-64px)] p-6 max-w-5xl mx-auto flex flex-col items-center">
        <!-- View Title Header -->
        <div class="glass-card text-center px-8 py-6 rounded-3xl mb-6 w-full max-w-3xl space-y-2 border border-white/30 dark:border-slate-700 shadow-2xl">
            <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-extrabold uppercase">
                <span>{{ esAdmin ? '⚡ Panel de Administración' : '💡 Sugerencias' }}</span>
            </div>
            <h1 class="font-extrabold text-3xl text-slate-900 dark:text-slate-100">
                {{ esAdmin ? 'Gestión de Sugerencias & Reportes' : 'Mis Sugerencias & Reportes' }}
            </h1>
            <p class="text-xs text-slate-600 dark:text-slate-300">
                {{ esAdmin ? 'Revisa, acepta o rechaza las propuestas de adición enviadas por la comunidad.' : 'Consulta el estado de revisión de tus propuestas enviadas.' }}
            </p>
        </div>

        <!-- Mandatory 30 Days Warning Note -->
        <div class="glass-card w-full max-w-3xl p-4 mb-6 rounded-2xl border-l-4 border-amber-500 bg-amber-500/10 text-amber-600 dark:text-amber-300 text-xs font-semibold flex items-center gap-2 shadow-md">
            <span>⚠️</span>
            <span>* Los reportes rechazados se eliminarán automáticamente después de 30 días.</span>
        </div>

        <!-- Filter Tabs -->
        <div class="flex flex-wrap items-center justify-center gap-2 mb-6 bg-slate-900/40 p-1.5 rounded-2xl border border-slate-700/50">
            <button 
                @click="filtroEstado = 'todos'" 
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer"
                :class="filtroEstado === 'todos' ? 'bg-amber-500 text-white shadow-md' : 'text-slate-300 hover:bg-white/10'"
            >
                Todos ({{ reportes.length }})
            </button>
            <button 
                @click="filtroEstado = 'pendiente'" 
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1"
                :class="filtroEstado === 'pendiente' ? 'bg-amber-500 text-white shadow-md' : 'text-slate-300 hover:bg-white/10'"
            >
                <span>⏳</span> En Revisión ({{ reportes.filter(r => r.estado === 'pendiente').length }})
            </button>
            <button 
                @click="filtroEstado = 'aceptado'" 
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1"
                :class="filtroEstado === 'aceptado' ? 'bg-emerald-500 text-white shadow-md' : 'text-slate-300 hover:bg-white/10'"
            >
                <span>✅</span> Aceptados ({{ reportes.filter(r => r.estado === 'aceptado').length }})
            </button>
            <button 
                @click="filtroEstado = 'rechazado'" 
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1"
                :class="filtroEstado === 'rechazado' ? 'bg-red-500 text-white shadow-md' : 'text-slate-300 hover:bg-white/10'"
            >
                <span>❌</span> Rechazados ({{ reportes.filter(r => r.estado === 'rechazado').length }})
            </button>
        </div>

        <!-- Loading State -->
        <div v-if="cargando" class="glass-card p-8 rounded-3xl text-center text-slate-600 dark:text-slate-300 max-w-md w-full my-8">
            <div class="text-3xl animate-spin mb-2">🌀</div>
            <p class="font-bold text-sm">Cargando sugerencias...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="reportesFiltrados.length === 0" class="glass-card p-10 rounded-3xl text-center max-w-md w-full my-8 space-y-3 shadow-xl">
            <span class="text-5xl">📋</span>
            <h2 class="font-extrabold text-xl text-slate-900 dark:text-slate-100">No hay sugerencias</h2>
            <p class="text-xs text-slate-600 dark:text-slate-300">No se encontraron solicitudes en esta categoría.</p>
        </div>

        <!-- Reports List -->
        <div v-else class="w-full max-w-3xl space-y-4">
            <div 
                v-for="r in reportesFiltrados" 
                :key="r.id" 
                class="glass-card p-6 rounded-3xl border border-white/30 dark:border-slate-700/80 shadow-xl space-y-4 relative transition-all hover:scale-[1.01]"
            >
                <!-- Top Status Header -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-700/80 pb-3">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">{{ r.tipo === 'personaje' ? '👤' : '🌀' }}</span>
                        <span class="font-extrabold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
                            {{ r.tipo === 'personaje' ? 'Personaje' : 'Beyblade' }}
                        </span>
                        <span class="text-slate-400">•</span>
                        <span class="text-xs text-slate-500 dark:text-slate-400">{{ r.created_at }}</span>
                    </div>

                    <!-- Status Badge -->
                    <div>
                        <span 
                            v-if="r.estado === 'pendiente'"
                            class="px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-extrabold flex items-center gap-1"
                        >
                            <span>⏳</span> En Revisión
                        </span>
                        <span 
                            v-else-if="r.estado === 'aceptado'"
                            class="px-3 py-1 bg-emerald-500/15 border border-emerald-500/40 text-emerald-600 dark:text-emerald-400 rounded-full text-xs font-extrabold flex items-center gap-1"
                        >
                            <span>✅</span> Aceptado
                        </span>
                        <span 
                            v-else
                            class="px-3 py-1 bg-red-500/15 border border-red-500/40 text-red-600 dark:text-red-400 rounded-full text-xs font-extrabold flex items-center gap-1"
                        >
                            <span>❌</span> Rechazado
                        </span>
                    </div>
                </div>

                <!-- Body Info -->
                <div class="space-y-2 text-slate-900 dark:text-slate-100">
                    <h3 class="text-xl font-extrabold text-slate-900 dark:text-slate-100">
                        {{ r.nombre }}
                    </h3>

                    <p v-if="r.descripcion" class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-white/40 dark:bg-slate-800/40 p-3 rounded-2xl border border-white/20 dark:border-slate-700/50">
                        {{ r.descripcion }}
                    </p>

                    <div v-if="r.opcional" class="text-xs text-amber-600 dark:text-amber-300 bg-amber-500/10 p-3 rounded-2xl border border-amber-500/20">
                        <span class="font-bold">Info adicional:</span> {{ r.opcional }}
                    </div>

                    <div v-if="esAdmin" class="text-[11px] text-slate-400 pt-1">
                        Sugerido por: <span class="font-bold text-slate-300">{{ r.usuario_nombre }} (@{{ r.username }})</span>
                    </div>
                </div>

                <!-- Admin Actions -->
                <div v-if="esAdmin && r.estado === 'pendiente'" class="pt-3 border-t border-slate-200 dark:border-slate-700/80 flex justify-end gap-3">
                    <button 
                        @click="responderReporte(r.id, 'rechazado')"
                        class="px-4 py-2 bg-red-500/15 hover:bg-red-500 text-red-600 dark:text-red-300 hover:text-white border border-red-500/40 rounded-xl text-xs font-extrabold transition-all flex items-center gap-1 cursor-pointer"
                    >
                        <span>❌</span> Rechazar
                    </button>
                    <button 
                        @click="responderReporte(r.id, 'aceptado')"
                        class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all flex items-center gap-1 cursor-pointer"
                    >
                        <span>✅</span> Aceptar Sugerencia
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
