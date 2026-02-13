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
    <div class="flex flex-col items-center justify-center gap-4 p-6">
        <div class="border-2 border-black p-6 bg-white rounded-lg">
            <h1 class="font-bold text-[24px] text-black">Crear Chat</h1>
        </div>
        <form action="post">
            <div class="flex flex-col items-center justify-center m-6 p-6 gap-4 border-2 border-black rounded-lg bg-white w-fit">
                
                    <div class="flex flex-col p-6 gap-4">
                        <h3 class="text-sm underline">Usuario para creación</h3>
                        <select class="bg-gray-200 w-[300px]" required v-model="usuario">
                            <option disabled selected>Selecciona un usuario</option>
                            <option v-for="usuario in usuariosFiltrados" :key="usuario.id" :value="usuario.id">{{ usuario.username }}</option>
                        </select>
                        <h3 class="text-sm underline">Nombre para el chat</h3>
                        <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                    </div>
                    <BaseButton color="cyan" @click="crearChat()">Crear</BaseButton>
                
            </div>
        </form>
    </div>
</template>