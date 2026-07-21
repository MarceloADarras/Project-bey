<script setup>
import api from './main';
import BaseButton from '../components/BaseButton.vue';
import Header from '../components/HeaderComponent.vue';
import LoadingOverlay from '../components/LoadingOverlay.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const nombre = ref('');
const apellido = ref('');
const correo = ref('');
const nombreUsuario = ref('');
const pass1 = ref('');
const pass2 = ref('');

const cargando = ref(false);
const mensajeCarga = ref('Procesando registro...');
const errorMsg = ref('');

const registrar = async() => {
    errorMsg.value = '';
    
    if (!nombreUsuario.value || !pass1.value) {
        errorMsg.value = 'Por favor completa los campos obligatorios.';
        return;
    }

    if (pass1.value !== pass2.value) {
        errorMsg.value = 'Las contraseñas no coinciden.';
        return;
    }

    try {
        cargando.value = true;
        mensajeCarga.value = 'Creando tu cuenta de Blader...';

        await api.post('/registration/', {
            first_name: nombre.value,
            last_name: apellido.value,
            email: correo.value,
            username: nombreUsuario.value,
            password1: pass1.value,
            password2: pass2.value
        });

        mensajeCarga.value = '¡Registro exitoso! Redirigiendo al Login...';
        
        setTimeout(() => {
            cargando.value = false;
            router.push('/iniciar');
        }, 1200);
        
    } catch(error) {
        cargando.value = false;
        console.error(error);
        errorMsg.value = error.response?.data?.detail || error.response?.data?.username?.[0] || 'Ocurrió un error durante el registro. Intenta nuevamente.';
    }
}
</script>

<template>
    <Header></Header>
    <LoadingOverlay :cargando="cargando" :mensaje="mensajeCarga" />
    
    <form @submit.prevent="registrar">
        <div class="flex justify-center items-center min-h-[calc(100vh-64px)] p-6">
            <div class="glass-card relative flex flex-col justify-center items-center p-8 gap-4 rounded-2xl w-full max-w-md shadow-xl text-slate-900">
                <h1 class="font-bold text-2xl mb-2 text-slate-900 dark:text-slate-100">Registro</h1>
                
                <div v-if="errorMsg" class="w-full p-3 bg-red-500/10 border border-red-500/40 rounded-xl text-red-600 dark:text-red-400 text-xs font-semibold text-center">
                    {{ errorMsg }}
                </div>

                <div class="flex flex-col gap-3 w-full">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="text" v-model="nombre">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Apellido</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="text" v-model="apellido">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Correo</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="email" v-model="correo">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre de usuario *</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="text" v-model="nombreUsuario" required>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Contraseña *</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="password" v-model="pass1" required>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Confirmar Contraseña *</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="password" v-model="pass2" required>
                    </div>
                </div>

                <div class="mt-4">
                    <BaseButton color="#FF6B35" hoverColor="#E63946" @click="registrar">Registrar</BaseButton>
                </div>
            </div>
        </div>
    </form>
</template>

