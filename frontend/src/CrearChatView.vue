<script setup>
import api from './main';
import BaseButton from '../components/BaseButton.vue';
import Header from '../components/HeaderComponent.vue';
import { ref, computed } from 'vue';

const usuario = ref();
const nombre = ref("");
const usuarios = ref([])
const user = localStorage.getItem('user')

const userInfo = JSON.parse(user);

const cargarUsuarios = async() => {
    try{
        const res = await api.get("cargar/usuarios")
        usuarios.value = res.data
    }catch(error){
        console.error(error);
    }
} 

const crearChat = async() => {
    try{
        const res = await api.post("crear/chat", {
            user_id: userInfo.id,
            id_usuario: usuario.value,
            nombre: nombre.value
        })
        console.log("Chat creado")
    }catch(error){
        console.error(error)
    }
}

const usuariosFiltrados = computed(() => {
    return usuarios.value.filter(
        usuario => usuario.id !== userInfo.id
    )
})
cargarUsuarios()
</script>
<template>
    <Header></Header>
    <div class="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] p-6">
        <form @submit.prevent="crearChat" class="w-full max-w-md">
            <div class="glass-card flex flex-col items-center justify-center p-8 gap-5 rounded-2xl shadow-xl text-slate-900 w-full">
                <h1 class="font-bold text-2xl text-slate-900">Crear Chat</h1>
                
                <div class="flex flex-col gap-4 w-full">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Usuario para creación</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" required v-model="usuario">
                            <option disabled value="" selected>Selecciona un usuario</option>
                            <option v-for="u in usuariosFiltrados" :key="u.id" :value="u.id">{{ u.username }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre para el chat</label>
                        <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required placeholder="Escribe el nombre del chat">
                    </div>
                </div>

                <div class="mt-4">
                    <BaseButton color="#FF6B35" hoverColor="#E63946" @click="crearChat()">Crear</BaseButton>
                </div>
            </div>
        </form>
    </div>
</template>
