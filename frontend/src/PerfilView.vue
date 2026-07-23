<script setup>
import { ref, onMounted } from 'vue';
import Header from '../components/HeaderComponent.vue';
import api from './main';
import { useRouter } from 'vue-router';

const router = useRouter();

const perfil = ref(null);
const cargando = ref(true);
const errorMsg = ref('');

// Form editar datos
const formDatos = ref({
    first_name: '',
    last_name: '',
    username: '',
    email: ''
});
const guardandoDatos = ref(false);
const mensajeDatos = ref({ tipo: '', texto: '' });

// Form cambiar contraseña
const passwordActual = ref('');
const passwordVerificada = ref(false);
const verificandoPassword = ref(false);
const mensajePassword = ref({ tipo: '', texto: '' });

const passwordNueva = ref('');
const passwordConfirmacion = ref('');
const cambiandoPassword = ref(false);

const localUserRaw = localStorage.getItem('user');
const localUser = localUserRaw ? JSON.parse(localUserRaw) : null;

const cargarPerfil = async () => {
    try {
        cargando.value = true;
        errorMsg.value = '';
        
        let endpoint = 'perfil/usuario';
        if (localUser && localUser.id) {
            endpoint = `perfil/usuario?user_id=${localUser.id}`;
        }
        
        const res = await api.get(endpoint);
        perfil.value = res.data;
        
        // Fill form fields
        formDatos.value.first_name = perfil.value.first_name || '';
        formDatos.value.last_name = perfil.value.last_name || '';
        formDatos.value.username = perfil.value.username || '';
        formDatos.value.email = perfil.value.email || '';

    } catch (error) {
        console.error('Error al cargar perfil:', error);
        if (localUser) {
            perfil.value = {
                id: localUser.id,
                username: localUser.username || 'Blader',
                email: localUser.email || 'N/A',
                full_name: `${localUser.first_name || ''} ${localUser.last_name || ''}`.trim() || localUser.username,
                date_joined: 'Reciente',
                chats_count: 0
            };
            formDatos.value.username = localUser.username || '';
            formDatos.value.email = localUser.email || '';
            formDatos.value.first_name = localUser.first_name || '';
            formDatos.value.last_name = localUser.last_name || '';
        } else {
            errorMsg.value = 'No se pudo cargar el perfil del usuario.';
        }
    } finally {
        cargando.value = false;
    }
};

const guardarPerfil = async () => {
    mensajeDatos.value = { tipo: '', texto: '' };
    if (!formDatos.value.username.trim()) {
        mensajeDatos.value = { tipo: 'error', texto: 'El nombre de usuario es obligatorio.' };
        return;
    }
    try {
        guardandoDatos.value = true;
        const payload = {
            user_id: perfil.value?.id,
            first_name: formDatos.value.first_name,
            last_name: formDatos.value.last_name,
            username: formDatos.value.username,
            email: formDatos.value.email
        };
        const res = await api.post('editar/perfil', payload);
        mensajeDatos.value = { tipo: 'exito', texto: res.data.message || 'Perfil actualizado correctamente.' };
        
        // Update local storage user if needed
        if (localUser) {
            localUser.username = formDatos.value.username;
            localUser.first_name = formDatos.value.first_name;
            localUser.last_name = formDatos.value.last_name;
            localUser.email = formDatos.value.email;
            localStorage.setItem('user', JSON.stringify(localUser));
        }

        await cargarPerfil();
    } catch (error) {
        const msg = error.response?.data?.error || 'Error al guardar cambios de perfil.';
        mensajeDatos.value = { tipo: 'error', texto: msg };
    } finally {
        guardandoDatos.value = false;
    }
};

const verificarPasswordActual = async () => {
    mensajePassword.value = { tipo: '', texto: '' };
    if (!passwordActual.value) {
        mensajePassword.value = { tipo: 'error', texto: 'Ingresa tu contraseña actual.' };
        return;
    }
    try {
        verificandoPassword.value = true;
        const payload = {
            user_id: perfil.value?.id,
            password_actual: passwordActual.value
        };
        const res = await api.post('verificar/password', payload);
        if (res.data.valid) {
            passwordVerificada.value = true;
            mensajePassword.value = { tipo: 'exito', texto: '✓ Contraseña actual verificada correctamente. Ya puedes ingresar tu nueva contraseña.' };
        } else {
            passwordVerificada.value = false;
            mensajePassword.value = { tipo: 'error', texto: res.data.error || 'La contraseña es incorrecta.' };
        }
    } catch (error) {
        passwordVerificada.value = false;
        const msg = error.response?.data?.error || 'Error al verificar la contraseña.';
        mensajePassword.value = { tipo: 'error', texto: msg };
    } finally {
        verificandoPassword.value = false;
    }
};

const guardarNuevaPassword = async () => {
    mensajePassword.value = { tipo: '', texto: '' };
    if (!passwordNueva.value) {
        mensajePassword.value = { tipo: 'error', texto: 'Ingresa la nueva contraseña.' };
        return;
    }
    if (passwordNueva.value.length < 6) {
        mensajePassword.value = { tipo: 'error', texto: 'La nueva contraseña debe tener al menos 6 caracteres.' };
        return;
    }
    if (passwordNueva.value !== passwordConfirmacion.value) {
        mensajePassword.value = { tipo: 'error', texto: 'Las contraseñas no coinciden.' };
        return;
    }

    try {
        cambiandoPassword.value = true;
        const payload = {
            user_id: perfil.value?.id,
            password_actual: passwordActual.value,
            password_nueva: passwordNueva.value,
            password_confirmacion: passwordConfirmacion.value
        };
        const res = await api.post('cambiar/password', payload);
        mensajePassword.value = { tipo: 'exito', texto: res.data.message || 'Contraseña actualizada con éxito.' };
        
        // Reset password fields
        passwordActual.value = '';
        passwordNueva.value = '';
        passwordConfirmacion.value = '';
        passwordVerificada.value = false;
    } catch (error) {
        const msg = error.response?.data?.error || 'Error al actualizar la contraseña.';
        mensajePassword.value = { tipo: 'error', texto: msg };
    } finally {
        cambiandoPassword.value = false;
    }
};

const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('auth_token');
    router.push('/home');
    window.location.reload();
};

onMounted(() => {
    cargarPerfil();
});
</script>

<template>
    <Header></Header>

    <div class="min-h-[calc(100vh-64px)] p-6 max-w-5xl mx-auto flex flex-col items-center">
        <!-- Loading State -->
        <div v-if="cargando" class="glass-card p-8 rounded-3xl text-center text-slate-600 dark:text-slate-300 max-w-md w-full shadow-2xl my-12">
            <div class="text-4xl animate-spin mb-3">🌀</div>
            <p class="font-bold text-sm">Cargando datos del perfil...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMsg" class="glass-card p-8 rounded-3xl text-center max-w-md w-full shadow-2xl space-y-4 my-12">
            <span class="text-4xl">⚠️</span>
            <h2 class="font-extrabold text-xl text-slate-900 dark:text-slate-100">Sesión no encontrada</h2>
            <p class="text-xs text-slate-600 dark:text-slate-300">{{ errorMsg }}</p>
            <router-link to="/iniciar" class="inline-block px-5 py-2.5 bg-amber-500 text-white rounded-xl text-xs font-bold no-underline shadow-md">
                Iniciar Sesión
            </router-link>
        </div>

        <!-- User Profile Card -->
        <div v-else class="w-full space-y-8">
            <!-- Header Banner Card -->
            <div class="glass-card relative overflow-hidden p-8 rounded-3xl shadow-2xl border border-white/30 dark:border-slate-700 flex flex-col sm:flex-row items-center gap-6">
                <div class="absolute -top-20 -left-20 w-64 h-64 bg-amber-500/20 rounded-full blur-3xl pointer-events-none"></div>
                <div class="absolute -bottom-20 -right-20 w-64 h-64 bg-orange-600/20 rounded-full blur-3xl pointer-events-none"></div>

                <!-- Avatar Container -->
                <div class="relative w-28 h-28 rounded-3xl bg-gradient-to-br from-amber-500 to-orange-600 p-1 flex items-center justify-center shadow-xl flex-shrink-0">
                    <div class="w-full h-full bg-slate-900 rounded-[22px] flex items-center justify-center text-5xl">
                        👤
                    </div>
                </div>

                <!-- Main Info -->
                <div class="flex-1 text-center sm:text-left space-y-1.5 text-slate-900 dark:text-slate-100">
                    <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/40 text-amber-600 dark:text-amber-400 rounded-full text-xs font-extrabold uppercase tracking-wider">
                        <span>⚡ Blader Oficial</span>
                        <span v-if="perfil.is_staff" class="ml-1 text-red-500">(Admin)</span>
                    </div>

                    <h1 class="text-3xl font-black text-slate-900 dark:text-slate-100">
                        {{ perfil.full_name || perfil.username }}
                    </h1>
                    
                    <p class="text-xs font-semibold text-amber-600 dark:text-amber-400">
                        @{{ perfil.username }} • {{ perfil.email || 'Sin correo' }}
                    </p>
                </div>

                <button 
                    type="button" 
                    @click="logout" 
                    class="px-4 py-2 bg-red-500/15 hover:bg-red-500 text-red-600 dark:text-red-400 hover:text-white border border-red-500/30 rounded-xl text-xs font-bold transition-all shadow-md flex items-center gap-1.5 cursor-pointer flex-shrink-0"
                >
                    <span>🚪</span> Cerrar Sesión
                </button>
            </div>

            <!-- Two Column Editing Sections -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
                
                <!-- SECTION 1: Editar Datos Personales -->
                <div class="glass-card p-6 sm:p-8 rounded-3xl border border-white/30 dark:border-slate-700 shadow-xl space-y-5">
                    <div class="border-b border-slate-200 dark:border-slate-700 pb-3 flex items-center gap-2">
                        <span class="text-2xl">📝</span>
                        <div>
                            <h2 class="font-extrabold text-xl text-slate-900 dark:text-slate-100">Datos Personales</h2>
                            <p class="text-xs text-slate-600 dark:text-slate-300">Modifica tus nombres, usuario y correo electrónico.</p>
                        </div>
                    </div>

                    <!-- Feedback Alert -->
                    <div 
                        v-if="mensajeDatos.texto" 
                        class="p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2"
                        :class="mensajeDatos.tipo === 'exito' ? 'bg-emerald-500/15 border border-emerald-500/40 text-emerald-600 dark:text-emerald-400' : 'bg-red-500/15 border border-red-500/40 text-red-600 dark:text-red-400'"
                    >
                        <span>{{ mensajeDatos.tipo === 'exito' ? '✅' : '⚠️' }}</span>
                        <span>{{ mensajeDatos.texto }}</span>
                    </div>

                    <form @submit.prevent="guardarPerfil" class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nombre(s)</label>
                                <input 
                                    type="text" 
                                    v-model="formDatos.first_name"
                                    placeholder="Tu nombre"
                                    class="w-full px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                                >
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Apellido(s)</label>
                                <input 
                                    type="text" 
                                    v-model="formDatos.last_name"
                                    placeholder="Tu apellido"
                                    class="w-full px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                                >
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nombre de Usuario *</label>
                            <div class="relative">
                                <span class="absolute left-3.5 top-2.5 text-slate-400 text-xs font-bold">@</span>
                                <input 
                                    type="text" 
                                    v-model="formDatos.username"
                                    required
                                    placeholder="usuario"
                                    class="w-full pl-8 pr-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner font-semibold"
                                >
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Correo Electrónico</label>
                            <input 
                                type="email" 
                                v-model="formDatos.email"
                                placeholder="tu@correo.com"
                                class="w-full px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                            >
                        </div>

                        <div class="pt-2">
                            <button 
                                type="submit" 
                                :disabled="guardandoDatos"
                                class="w-full py-2.5 px-4 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all hover:scale-[1.02] flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                            >
                                <span v-if="guardandoDatos" class="animate-spin">🌀</span>
                                <span>{{ guardandoDatos ? 'Guardando...' : '💾 Guardar Datos' }}</span>
                            </button>
                        </div>
                    </form>
                </div>

                <!-- SECTION 2: Cambiar Contraseña (Secuencial con Verificación) -->
                <div class="glass-card p-6 sm:p-8 rounded-3xl border border-white/30 dark:border-slate-700 shadow-xl space-y-5">
                    <div class="border-b border-slate-200 dark:border-slate-700 pb-3 flex items-center gap-2">
                        <span class="text-2xl">🔑</span>
                        <div>
                            <h2 class="font-extrabold text-xl text-slate-900 dark:text-slate-100">Cambiar Contraseña</h2>
                            <p class="text-xs text-slate-600 dark:text-slate-300">Verifica tu contraseña actual para ingresar la nueva.</p>
                        </div>
                    </div>

                    <!-- Feedback Alert -->
                    <div 
                        v-if="mensajePassword.texto" 
                        class="p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2"
                        :class="mensajePassword.tipo === 'exito' ? 'bg-emerald-500/15 border border-emerald-500/40 text-emerald-600 dark:text-emerald-400' : 'bg-red-500/15 border border-red-500/40 text-red-600 dark:text-red-400'"
                    >
                        <span>{{ mensajePassword.tipo === 'exito' ? '✅' : '⚠️' }}</span>
                        <span>{{ mensajePassword.texto }}</span>
                    </div>

                    <!-- Paso 1: Ingresar y verificar Contraseña Actual -->
                    <div class="space-y-3 bg-white/40 dark:bg-slate-800/40 p-4 rounded-2xl border border-slate-200 dark:border-slate-700">
                        <label class="block text-xs font-bold text-slate-800 dark:text-slate-200">
                            Paso 1: Contraseña Actual *
                        </label>
                        <div class="flex items-center gap-2">
                            <input 
                                type="password" 
                                v-model="passwordActual"
                                :disabled="passwordVerificada"
                                placeholder="••••••••"
                                class="flex-1 px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner disabled:opacity-60"
                            >
                            <button 
                                type="button"
                                v-if="!passwordVerificada"
                                @click="verificarPasswordActual"
                                :disabled="verificandoPassword || !passwordActual"
                                class="px-4 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center gap-1.5 cursor-pointer disabled:opacity-50 flex-shrink-0"
                            >
                                <span v-if="verificandoPassword" class="animate-spin">🌀</span>
                                <span>Verificar</span>
                            </button>
                            <span v-else class="px-3 py-2 bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 rounded-xl text-xs font-extrabold border border-emerald-500/40 flex items-center gap-1">
                                ✓ Visto bueno
                            </span>
                        </div>
                    </div>

                    <!-- Paso 2: Ingresar Nueva Contraseña (solo visible si verificada) -->
                    <form v-if="passwordVerificada" @submit.prevent="guardarNuevaPassword" class="space-y-4 pt-1 transition-all animate-fadeIn">
                        <div class="bg-amber-500/10 border border-amber-500/30 p-3 rounded-xl text-xs font-bold text-amber-600 dark:text-amber-400 flex items-center gap-1.5">
                            <span>🔓</span> Paso 2: Ingresa y confirma tu nueva contraseña
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nueva Contraseña *</label>
                            <input 
                                type="password" 
                                v-model="passwordNueva"
                                required
                                placeholder="Mínimo 6 caracteres"
                                class="w-full px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                            >
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Repetir Nueva Contraseña *</label>
                            <input 
                                type="password" 
                                v-model="passwordConfirmacion"
                                required
                                placeholder="Repite la nueva contraseña"
                                class="w-full px-3.5 py-2.5 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:border-amber-500 focus:outline-none transition-colors shadow-inner"
                            >
                        </div>

                        <div class="pt-2">
                            <button 
                                type="submit" 
                                :disabled="cambiandoPassword"
                                class="w-full py-2.5 px-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white rounded-xl text-xs font-extrabold shadow-lg transition-all hover:scale-[1.02] flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                            >
                                <span v-if="cambiandoPassword" class="animate-spin">🌀</span>
                                <span>{{ cambiandoPassword ? 'Actualizando...' : '🔒 Actualizar Contraseña' }}</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
