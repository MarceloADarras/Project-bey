<script setup>
import Header from '../components/HeaderComponent.vue';
import { onMounted, ref, computed } from 'vue';
import api from './main.js';

const ActiveUserJson = localStorage.getItem('user');
const ActiveUser = ActiveUserJson ? JSON.parse(ActiveUserJson) : null;
const esAdmin = computed(() => ActiveUser?.is_staff || ActiveUser?.is_superuser || false);

const usuarios = ref([]);
const cargando = ref(true);
const busqueda = ref('');

// Password Modal State
const mostrarModal = ref(false);
const usuarioSeleccionado = ref(null);
const nuevaPassword = ref('');
const confirmPassword = ref('');
const cambiando = ref(false);
const mensajeModal = ref({ tipo: '', texto: '' });

// Admin modal state
const mostrarModalAdmin = ref(false);

const cargarUsuarios = async () => {
    try {
        cargando.value = true;
        if (!esAdmin.value) return;

        const res = await api.get("cargar/usuarios");
        usuarios.value = res?.data || [];
    } catch (e) {
        console.error("Error al cargar los usuarios:", e);
    } finally {
        cargando.value = false;
    }
};

const usuariosFiltrados = computed(() => {
    if (!busqueda.value.trim()) return usuarios.value;
    const q = busqueda.value.toLowerCase().trim();
    return usuarios.value.filter(u => 
        (u.username && u.username.toLowerCase().includes(q)) ||
        (u.nombre && u.nombre.toLowerCase().includes(q)) ||
        (u.correo && u.correo.toLowerCase().includes(q))
    );
});

const abrirModalCambiarPass = (user) => {
    usuarioSeleccionado.value = user;
    nuevaPassword.value = '';
    confirmPassword.value = '';
    mensajeModal.value = { tipo: '', texto: '' };
    mostrarModal.value = true;
};

const abrirModalAdmin = (user) => {
    usuarioSeleccionado.value = user;
    mensajeModal.value = { tipo: '', texto: '' };
    mostrarModalAdmin.value = true;
};

const cerrarModal = () => {
    mostrarModal.value = false;
    usuarioSeleccionado.value = null;
};

const cerrarModalAdmin = () => {
    mostrarModalAdmin.value = false;
    usuarioSeleccionado.value = null;
};

const ejecutarCambioPassword = async () => {
    if (!usuarioSeleccionado.value) return;
    
    if (!nuevaPassword.value || nuevaPassword.value.length < 6) {
        mensajeModal.value = { tipo: 'error', texto: 'La contraseña debe tener al menos 6 caracteres.' };
        return;
    }

    if (nuevaPassword.value !== confirmPassword.value) {
        mensajeModal.value = { tipo: 'error', texto: 'Las contraseñas no coinciden.' };
        return;
    }

    try {
        cambiando.value = true;
        mensajeModal.value = { tipo: '', texto: '' };

        const payload = {
            target_user_id: usuarioSeleccionado.value.id,
            nueva_password: nuevaPassword.value,
            admin_id: ActiveUser?.id
        };

        const res = await api.post("admin/cambiar/password", payload);
        mensajeModal.value = { tipo: 'exito', texto: res.data.message || 'Contraseña actualizada con éxito.' };

        setTimeout(() => {
            cerrarModal();
            cargarUsuarios();
        }, 1300);

    } catch (error) {
        console.error("Error al cambiar contraseña:", error);
        mensajeModal.value = { 
            tipo: 'error', 
            texto: error.response?.data?.error || 'Error al cambiar la contraseña del usuario.' 
        };
    } finally {
        cambiando.value = false;
    }
};

const ejecutarCambioAdmin = async () => {
    if (!usuarioSeleccionado.value) return;

    try {
        cambiando.value = true;
        mensajeModal.value = { tipo: '', texto: '' };

        const payload = {
            target_user_id: usuarioSeleccionado.value.id,
            admin_id: ActiveUser?.id
        };

        const res = await api.post("admin/dar/admin", payload);
        mensajeModal.value = { tipo: 'exito', texto: res.data.message || 'Permisos de administrador otorgados con éxito.' };

        setTimeout(() => {
            cerrarModalAdmin();
            cargarUsuarios();
        }, 1300);

    } catch (e) {
        console.error("Error al dar permisos:", e);
        mensajeModal.value = { 
            tipo: 'error', 
            texto: e.response?.data?.error || 'Error al dar permisos de administrador.' 
        };
    } finally {
        cambiando.value = false;
    }
};

onMounted(() => {
    cargarUsuarios();
});
</script>

<template>
    <Header />

    <!-- Main Container -->
    <div v-if="esAdmin" class="min-h-[calc(100vh-64px)] p-4 sm:p-8 max-w-6xl mx-auto flex flex-col items-center">
        <!-- Title Banner -->
        <div class="glass-card text-center px-8 py-6 rounded-3xl mb-8 w-full max-w-4xl space-y-2 border border-white/30 dark:border-slate-700/80 shadow-2xl">
            <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-extrabold uppercase">
                <span>⚡ Panel de Administración</span>
            </div>
            <h1 class="font-extrabold text-3xl text-slate-900 dark:text-slate-100">Gestión de Usuarios</h1>
            <p class="text-xs text-slate-600 dark:text-slate-300">
                Visualiza los usuarios registrados, administra roles y restablece contraseñas de emergencia.
            </p>
        </div>

        <!-- Search & Info Bar -->
        <div class="w-full max-w-4xl flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
            <div class="relative w-full sm:w-80">
                <input 
                    type="text" 
                    v-model="busqueda"
                    placeholder="🔍 Buscar por usuario, nombre o correo..." 
                    class="w-full px-4 py-2.5 bg-white/80 dark:bg-slate-900/80 border border-slate-300 dark:border-slate-700/80 rounded-2xl text-xs text-slate-900 dark:text-white placeholder-slate-500 dark:placeholder-slate-400 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                >
            </div>

            <div class="px-4 py-2 bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700/60 rounded-xl text-xs text-slate-800 dark:text-slate-300 font-semibold flex items-center gap-2 shadow-sm">
                <span>👥 Total:</span>
                <span class="text-amber-600 dark:text-amber-400 font-extrabold">{{ usuariosFiltrados.length }} usuarios</span>
            </div>
        </div>

        <!-- Loading -->
        <div v-if="cargando" class="glass-card p-10 rounded-3xl text-center text-slate-700 dark:text-slate-300 max-w-md w-full my-8">
            <div class="text-3xl animate-spin mb-2">🌀</div>
            <p class="font-bold text-sm">Cargando lista de usuarios...</p>
        </div>

        <!-- Users Table -->
        <div v-else class="w-full max-w-4xl glass-card bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700/80 rounded-3xl overflow-hidden shadow-2xl">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-100/90 dark:bg-slate-800/80 text-amber-600 dark:text-amber-500 text-xs uppercase font-extrabold tracking-wider border-b border-slate-200 dark:border-slate-700/80">
                            <th class="py-3.5 px-5">ID</th>
                            <th class="py-3.5 px-5">Usuario</th>
                            <th class="py-3.5 px-5">Nombre</th>
                            <th class="py-3.5 px-5">Correo Electrónico</th>
                            <th class="py-3.5 px-5">Rol</th>
                            <th class="py-3.5 px-5 text-center">Acciones</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 dark:divide-slate-800/80 text-xs text-slate-800 dark:text-slate-200">
                        <tr 
                            v-for="u in usuariosFiltrados" 
                            :key="u.id"
                            class="hover:bg-slate-100/60 dark:hover:bg-white/5 transition-colors"
                        >
                            <td class="py-4 px-5 font-mono text-slate-500 dark:text-slate-400">#{{ u.id }}</td>
                            <td class="py-4 px-5 font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                                <span class="w-7 h-7 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold text-xs">
                                    {{ (u.username || 'U')[0].toUpperCase() }}
                                </span>
                                <span class="text-slate-900 dark:text-slate-100 font-extrabold">@{{ u.username }}</span>
                            </td>
                            <td class="py-4 px-5 text-slate-800 dark:text-slate-300 font-medium">{{ u.nombre || '-' }}</td>
                            <td class="py-4 px-5 text-slate-600 dark:text-slate-400">{{ u.correo || 'Sin correo' }}</td>
                            <td class="py-4 px-5">
                                <span 
                                    v-if="u.is_superuser || u.is_staff" 
                                    class="px-2.5 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-700 dark:text-amber-300 rounded-full text-[10px] font-extrabold flex items-center gap-1 w-fit"
                                >
                                    <span>⚡</span> Admin
                                </span>
                                <span 
                                    v-else 
                                    class="px-2.5 py-1 bg-slate-200 dark:bg-slate-700/50 border border-slate-300 dark:border-slate-600/50 text-slate-700 dark:text-slate-300 rounded-full text-[10px] font-semibold flex items-center gap-1 w-fit"
                                >
                                    <span>👤</span> Usuario
                                </span>
                            </td>
                            <td class="py-4 px-5 text-center">
                                <div class="flex flex-col sm:flex-row items-center justify-center gap-2">
                                    <button 
                                        @click="abrirModalCambiarPass(u)"
                                        class="px-3 py-1.5 bg-amber-500/15 hover:bg-amber-500 text-amber-700 dark:text-amber-300 hover:text-white border border-amber-500/40 rounded-xl text-xs font-bold transition-all hover:scale-105 flex items-center gap-1 cursor-pointer shadow-sm"
                                        title="Cambiar contraseña de emergencia"
                                    >
                                        <span>🔑</span> Contraseña
                                    </button>

                                    <button 
                                        v-if="!u.is_superuser && !u.is_staff" 
                                        @click="abrirModalAdmin(u)"
                                        class="px-3 py-1.5 bg-indigo-500/15 hover:bg-indigo-600 text-indigo-700 dark:text-indigo-300 hover:text-white border border-indigo-500/40 rounded-xl text-xs font-bold transition-all hover:scale-105 flex items-center gap-1 cursor-pointer shadow-sm"
                                        title="Otorgar permisos de administrador"
                                    >
                                        <span>⚡</span> Hacer Admin
                                    </button>
                                </div>
                            </td>
                        </tr>

                        <tr v-if="usuariosFiltrados.length === 0">
                            <td colspan="6" class="py-8 text-center text-slate-500 dark:text-slate-400 text-xs">
                                No se encontraron usuarios que coincidan con la búsqueda.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>


        <!-- Emergency Change Password Modal -->
        <div v-if="mostrarModal" class="fixed inset-0 bg-black/75 backdrop-blur-md flex items-center justify-center p-4 z-50">
            <div class="glass-card bg-slate-900/95 border border-slate-700/80 rounded-3xl p-6 sm:p-8 max-w-md w-full text-slate-100 shadow-2xl space-y-6">
                <!-- Modal Header -->
                <div class="flex items-center justify-between border-b border-slate-700 pb-4">
                    <div class="flex items-center gap-2">
                        <span class="text-2xl">🔑</span>
                        <div>
                            <h2 class="font-extrabold text-lg">Cambiar Contraseña</h2>
                            <p class="text-xs text-amber-400 font-semibold mt-0.5">
                                Usuario: @{{ usuarioSeleccionado?.username }}
                            </p>
                        </div>
                    </div>
                    <button 
                        @click="cerrarModal" 
                        class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                    >
                        ✕
                    </button>
                </div>

                <!-- Alert Message -->
                <div 
                    v-if="mensajeModal.texto" 
                    class="p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2"
                    :class="mensajeModal.tipo === 'exito' ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-300' : 'bg-red-500/20 border border-red-500/40 text-red-300'"
                >
                    <span>{{ mensajeModal.tipo === 'exito' ? '✅' : '⚠️' }}</span>
                    <span>{{ mensajeModal.texto }}</span>
                </div>

                <!-- Password Form -->
                <form @submit.prevent="ejecutarCambioPassword" class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Nueva Contraseña *</label>
                        <input 
                            type="password" 
                            v-model="nuevaPassword" 
                            required
                            placeholder="Mínimo 6 caracteres" 
                            class="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                        >
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Confirmar Nueva Contraseña *</label>
                        <input 
                            type="password" 
                            v-model="confirmPassword" 
                            required
                            placeholder="Repite la nueva contraseña" 
                            class="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white focus:border-amber-500 focus:outline-none transition-colors"
                        >
                    </div>

                    <div class="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-[11px] text-amber-300 font-semibold leading-relaxed">
                        ⚠️ <span class="font-bold">Atención:</span> Esta acción restablecerá la contraseña del usuario de forma inmediata sin necesidad de verificar su contraseña actual.
                    </div>

                    <!-- Actions -->
                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button 
                            type="button" 
                            @click="cerrarModal" 
                            class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-bold transition-colors"
                        >
                            Cancelar
                        </button>
                        <button 
                            type="submit" 
                            :disabled="cambiando"
                            class="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                        >
                            <span v-if="cambiando" class="animate-spin">🌀</span>
                            <span>{{ cambiando ? 'Guardando...' : 'Restablecer Contraseña' }}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Grant Admin Permissions Modal -->
        <div v-if="mostrarModalAdmin" class="fixed inset-0 bg-black/75 backdrop-blur-md flex items-center justify-center p-4 z-50">
            <div class="glass-card bg-slate-900/95 border border-slate-700/80 rounded-3xl p-6 sm:p-8 max-w-md w-full text-slate-100 shadow-2xl space-y-6">
                <div class="flex items-center justify-between border-b border-slate-700 pb-4">
                    <div class="flex items-center gap-2">
                        <span class="text-2xl">⚡</span>
                        <div>
                            <h2 class="font-extrabold text-lg">Asignar Rol Administrador</h2>
                            <p class="text-xs text-amber-400 font-semibold mt-0.5">
                                Usuario: @{{ usuarioSeleccionado?.username }}
                            </p>
                        </div>
                    </div>
                    <button 
                        @click="cerrarModalAdmin" 
                        class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                    >
                        ✕
                    </button>
                </div>

                <div 
                    v-if="mensajeModal.texto" 
                    class="p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2"
                    :class="mensajeModal.tipo === 'exito' ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-300' : 'bg-red-500/20 border border-red-500/40 text-red-300'"
                >
                    <span>{{ mensajeModal.tipo === 'exito' ? '✅' : '⚠️' }}</span>
                    <span>{{ mensajeModal.texto }}</span>
                </div>

                <form @submit.prevent="ejecutarCambioAdmin" class="space-y-4">
                    <div class="p-3.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-[11px] text-indigo-300 font-semibold leading-relaxed">
                        ⚡ <span class="font-bold">Confirmación:</span> Esta acción otorgará permisos de Administrador (`is_staff`) a @{{ usuarioSeleccionado?.username }}, permitiéndole crear, editar, eliminar registros y administrar sugerencias.
                    </div>

                    <!-- Actions -->
                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button 
                            type="button" 
                            @click="cerrarModalAdmin" 
                            class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-bold transition-colors"
                        >
                            Cancelar
                        </button>
                        <button 
                            type="submit" 
                            :disabled="cambiando"
                            class="px-6 py-2.5 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                        >
                            <span v-if="cambiando" class="animate-spin">🌀</span>
                            <span>{{ cambiando ? 'Otorgando...' : 'Asignar Admin' }}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Access Denied Screen -->
    <div v-else class="min-h-[calc(100vh-64px)] flex items-center justify-center p-6">
        <div class="glass-card p-10 rounded-3xl text-center max-w-md w-full space-y-4 shadow-2xl">
            <span class="text-5xl">🔒</span>
            <h1 class="font-extrabold text-2xl text-slate-900 dark:text-slate-100">Acceso Restringido</h1>
            <p class="text-xs text-slate-600 dark:text-slate-300">
                Lo sentimos, esta vista es exclusiva para administradores del sistema.
            </p>
            <router-link to="/home" class="inline-block px-5 py-2.5 bg-amber-500 text-white font-bold rounded-xl text-xs shadow-md">
                Volver al Inicio
            </router-link>
        </div>
    </div>
</template>

<style scoped>
</style>


<style scoped>
</style>
