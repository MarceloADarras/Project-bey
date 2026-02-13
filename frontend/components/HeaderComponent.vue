
<script setup>
import { ref } from 'vue'

const open = ref(false)
const user= localStorage.getItem('user')
const logout = async() => {
    try{
        if(user){
            localStorage.removeItem('user')
            localStorage.removeItem('auth_token')
        }
    } catch(error){
        console.error(error)
    }
}
</script>
<template>
    <header class="header">
        <div>
            <div>
                <router-link class="inline-block text-white font-bold text-[20px] rounded-[5px] bg-gray-700 no-underline transition-all duration-300 ease-in-out px-2 py-1 shadow-[0_2px_4px_rgba(0,0,0,0.3)] text-shadow hover:scale-110" :to="{name: 'Home'}">
                    <img class="w-24 h-auto" src="/img/BeyStory2.png" alt="">
                </router-link>
            </div>
        </div>
        <nav v-if="user" class="opciones">
            <transition
                enter-active-class="transition transform duration-300 ease-out"
                enter-from-class="translate-x-full opacity-0"
                enter-to-class="translate-x-0 opacity-100"
                leave-active-class="transition transform duration-300 ease-in"
                leave-from-class="translate-x-0 opacity-100"
                leave-to-class="translate-x-full opacity-0"
            >
                <div v-if="open" class="absolute top-0 right-0 w-64 h-full bg-gray-700 border-2 border-black shadow-lg p-6 transition-ease z-50">
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'bey'}}">Crear Beyblade</router-link>
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'fusion'}}">Crear Fusion Wheel</router-link>
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'clear'}}">Crear Clear Wheel</router-link>
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'track'}}">Crear Spin track</router-link>
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'tip'}}">Crear Tip</router-link>
                    <router-link class="block px-4 py-2 hover:bg-gray-100" :to="{name: 'Create', params: {nombre: 'tipe'}}">Crear Tipe</router-link>
                </div>
            </transition>
            <router-link class="link" :to="{name: 'Chats'}">Ir a chats</router-link>
            
            <a href="crear" type="button">Ventas</a>
            <router-link to="/home">
                <a type="button" @click="logout()">LogOut</a>
            </router-link>
            <button @click="open = !open" class="flex items-center gap-2 px-4 py-2 bg-gray-800 text-white rounded-lg hover:scale-110 transition transform duration-100 ease-in relative z-50">☰</button>
        </nav>
    </header>
</template>

<style>
    html body{
        margin: 0;
        padding: 0;
    }
    .header{
        display: flex;
        background: linear-gradient(135deg, #E63946 0%, #FF6B35 50%, #FFA500 100%);
        padding: 1%;
        align-items: center;
        justify-content: space-between;
        height: 70px;
        padding: 0 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-bottom: 3px solid #708090;
    }

    .title .link:hover{
        transform: scale(1.1);
        background: linear-gradient(45deg, #2c3e50 0%, #34495e 100%);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }

    .opciones{
        display: flex;
        justify-content: right;
        align-items: center;
    }

    .opciones a{
        text-decoration: none;
        margin: 5px;
        margin-right: 20px;
        color: white;
        font-size: large;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        padding: 4px 8px;
        border-radius: 4px;
    }

    .opciones a:hover{
        color: #FFA500;
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-1px);
    }

    body{
        margin: 0;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }

    body::before{
        content: "";
        position: fixed;
        inset: -50%;
        z-index: -1;

        background-image: linear-gradient(
            rgba(0,0,0,0.6),
            rgba(0,0,0,0.6)
        ), url("/img/Beyblade_logo.jfif");
        background-size: 15%;
        background-position: center;
        background-repeat: repeat;


        transform: rotate(-20deg);
       
    }

</style>

