<script setup>
import Header from "../components/HeaderComponent.vue"
import BaseButton from "../components/BaseButton.vue";
import LoadingOverlay from "../components/LoadingOverlay.vue";
import api from "./main";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref('');
const pass = ref('');

const cargando = ref(false);
const mensajeCarga = ref('Verificando credenciales...');
const errorMsg = ref('');

const login = async() => {
    errorMsg.value = '';
    
    if (!username.value || !pass.value) {
        errorMsg.value = 'Ingresa tu usuario y contraseña.';
        return;
    }

    try {
        cargando.value = true;
        mensajeCarga.value = 'Iniciando sesión...';

        const response = await api.post('auth/login/', {
            username: username.value,
            password: pass.value
        });

        const access = response.data?.token?.access || response.data?.access || response.data?.token;
        const user = response.data?.user;

        if (access) {
            localStorage.setItem("auth_token", typeof access === 'string' ? access : JSON.stringify(access));
            if (user) {
                localStorage.setItem("user", typeof user === 'string' ? user : JSON.stringify(user));
            } else {
                localStorage.setItem("user", JSON.stringify({ username: username.value }));
            }

            mensajeCarga.value = '¡Sesión verificada! Redirigiendo a la pantalla principal...';
            
            setTimeout(() => {
                cargando.value = false;
                router.push('/home');
            }, 1000);
        } else {
            cargando.value = false;
            errorMsg.value = 'Respuesta inesperada del servidor. Intenta de nuevo.';
        }

    } catch(error) {
        cargando.value = false;
        console.error(error);
        errorMsg.value = error.response?.data?.detail || error.response?.data?.non_field_errors?.[0] || 'Nombre de usuario o contraseña incorrectos.';
    }
}
</script>

<template>
    <Header></Header>
    <LoadingOverlay :cargando="cargando" :mensaje="mensajeCarga" />
    
    <form @submit.prevent="login">
        <div class="flex items-center justify-center min-h-[calc(100vh-64px)] p-6">
            <div class="glass-card relative flex flex-col items-center p-8 gap-5 rounded-2xl w-full max-w-md shadow-xl text-slate-900">
                <h1 class="font-bold text-2xl mb-2 text-slate-900 dark:text-slate-100">Iniciar sesión</h1>
                
                <div v-if="errorMsg" class="w-full p-3 bg-red-500/10 border border-red-500/40 rounded-xl text-red-600 dark:text-red-400 text-xs font-semibold text-center">
                    {{ errorMsg }}
                </div>

                <div class="flex flex-col gap-3 w-full">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre de usuario</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="text" v-model="username" required>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Contraseña</label>
                        <input class="w-full border border-slate-300 px-3 py-2 rounded-xl bg-white/90 text-slate-900 focus:outline-none focus:border-amber-500 transition-colors shadow-inner" type="password" v-model="pass" required>
                    </div>
                </div>
                
                <div class="mt-4">
                    <BaseButton color="#FF6B35" hoverColor="#E63946" @click="login()">Iniciar</BaseButton>
                </div>
            </div>
        </div>
    </form>
</template>

