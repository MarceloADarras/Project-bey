<script setup>
import Header from "../components/HeaderComponent.vue"
import BaseButton from "../components/BaseButton.vue";
import api from "./main";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter()

const username = ref('')
const pass = ref('')

const login = async() => {
    try{
        console.log(username.value, pass.value)
        return await api.post('auth/login/', {
            username: username.value,
            password: pass.value
        }).then(response =>{
            const access = response.data.token.access;
            const user = response.data.user;

            if(access){
                localStorage.setItem("auth_token", access)
                localStorage.setItem("user", JSON.stringify(user))
                router.push('/home')
            }
        })

    }catch(error){
        console.error(error)
    }
}
</script>
<template>
    <Header></Header>
    <form>
        <div class="flex items-center justify-center">
            <div class="relative flex flex-col items-center p-6 m-6 gap-4 border-2 border-black rounded-lg bg-white w-fit">
                <h1 class="font-bold text-[24px]">Iniciar sesion</h1>
                <div class="flex flex-col gap-2 w-full">
                    <h3 class="text-sm">Nombre de usuario</h3>
                    <input class="border-1 border-black px-2 py-1 rounded w-64 bg-gray-200" type="text" v-model="username">
                    <h3 class="text-sm">Contraseña</h3>
                    <input class="border-1 border-black px-2 py-1 rounded w-64 bg-gray-200" type="password" v-model="pass">
                </div>
                <BaseButton :color="'Cyan'" :hover-color="'Red'" @click="login()">Iniciar</BaseButton>
            </div>
        </div>
    </form>
    
</template>