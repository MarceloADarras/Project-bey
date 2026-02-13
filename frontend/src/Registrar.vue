<script setup>
import api from './main';
import BaseButton from '../components/BaseButton.vue';
import Header from '../components/HeaderComponent.vue';
import { ref } from 'vue';

const nombre = ref('')
const apellido = ref('')
const correo = ref('')
const nombreUsuario = ref('')
const pass1 = ref('')
const pass2 = ref('')

const registrar = async() => {
    try{
        if(pass1.value == pass2.value){
            await api.post('/registration/', {
                first_name: nombre.value,
                last_name: apellido.value,
                email: correo.value,
                username: nombreUsuario.value,
                password1: pass1.value,
                password2: pass2.value
            })
            console.log("Registro exitoso")
        }
        
    } catch(error){
        console.error(error)
    }
}
</script>
<template>
    <Header></Header>
    <form>
        <div class="flex justify-center">
            <div class="relative flex flex-col justify-center items-center border-2 border-black m-6 p-6 gap-4 rounded-lg bg-white w-fit">
                <h1 class="font-bold text-[24px]">Registro</h1>
                <div class="text-black">
                    <h3 class="text-sm">Nombre</h3>
                    <input class="bg-gray-200" type="text" v-model="nombre">
                    <h3 class="text-sm">Apellido</h3>
                    <input class="bg-gray-200" type="text" v-model="apellido">
                    <h3 class="text-sm">Correo</h3>
                    <input class="bg-gray-200" type="text" v-model="correo">
                    <h3 class="text-sm">Nombre de usuario</h3>
                    <input class="bg-gray-200" type="text" v-model="nombreUsuario">
                    <h3 class="text-sm">Contraseña</h3>
                    <input class="bg-gray-200" type="text" v-model="pass1">
                    <h3 class="text-sm">Confirmar Contraseña</h3>
                    <input class="bg-gray-200" type="text" v-model="pass2">
                </div>
                <BaseButton :color="'Cyan'" @accion="registrar">Rergistrar</BaseButton>
            </div>
        </div>
    </form>
    
</template>