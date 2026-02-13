<script setup>
import api from './main';
import BaseButton from '../components/BaseButton.vue';
import Header from '../components/HeaderComponent.vue';
import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
import { ref } from 'vue';

const chats = ref([]);

const mensaje = ref("");
const mensajes = ref([]);

const chatOpen = ref(false);
const showInfo = ref(false);

const cargarChats = async() => {
    try{
        const res = await api.get("cargar/chats")

        chats.value = res.data
        console.log(chats.value)
    }catch(error){
        console.error(error)
    }
}

const enviarMensaje = async() => {
    if(!mensaje.value.trim()) return

    mensajes.value.push({ role: "user", text: mensaje.value})

    const res = await api.post("beybot/chat", {
        mensaje: mensaje.value
    })

    mensajes.value.push({
        role: "bot",
        text: res.data.respuesta
    })

    mensaje.value = ""
}

cargarChats()
</script>
<template>
    <Header></Header>
    <div class="flex justify-end p-6">
        <button @click="chatOpen = !chatOpen" class="electric-button border-2 border-black rounded-xl p-6 bg-green-800 hover:scale-110 transition-all duration-200 hover:brightness-125">🤖</button>
    </div>
    <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-4"
    >
        <div
            v-if="chatOpen"
            class=" energy-box fixed bottom-24 right-6 w-80 h-96 bg-white border-2 border-black rounded-xl shadow-2xl flex flex-col z-40"
        >
            <div class="bg-blue-600 text-white p-3 rounded-t-xl flex justify-between items-center">
                <div class="flex items-center gap-2 cursor-pointer" @click="showInfo = !showInfo">
                    <span class="robot-avatar text-2xl">🤖</span>
                    <span class="font-bold">BeyBot</span>
                </div>
                <button @click="chatOpen = false" class=" rounded-lg p-2 hover:bg-red-900 transition-all transform duration-200 hover:scale-110 ">✖</button>
            </div>
            <transition
                enter-active-class="transition duration-300"
                enter-from-class="opacity-0 translate-y-2"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition duration-200"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
            >
                <div
                    v-if="showInfo"
                    class="absolute top-14 right-4 bg-white text-black text-xs p-3 rounded-lg shadow-lg w-60"
                >
                    ⚡ Soy BeyBot, tu asistente de BeyStory.
                    Puedo ayudarte a buscar beyblades, explicar piezas
                    y guiarte en tus batallas.
                </div>
            </transition>

            <div class="flex-1 p-3 overflow-y-auto text-sm">
                <p v-if="!mensaje" class="text-gray-500">Bienvenido Blader ⚡</p>
                <div v-for="(m, index) in mensajes" :key="index" class="gap-4">
                    <div v-if="m.role === 'user'" class="flex justify-end">
                        <div  class="flex justify-right border px-4 py-2 rounded-lg bg-blue-500 w-fit">
                            <p >{{ m.text }}</p>
                        </div>
                    </div>
                    <div v-else class="flex justify-start border px-4 py-2 rounded-lg bg-gray-300 w-fit">
                        <p>{{ m.text }}</p>
                </div>
            </div>
            </div>

            <div class="p-3 border-t flex gap-2">
                <input type="text" placeholder="Escribe un mensaje..." class="flex-1 border rounded px-2 py-1 text-sm" v-model="mensaje">
                <button class="bg-blue-500 text-white px-3 rounded hover:bg-blue-700 transition duration-200" @click="enviarMensaje()">➤</button>
            </div>
        </div>
    </transition>
    <div class="flex items-center justify-center gap-4 p-6">
        <div class="flex flex-col justify-center gap-4 p-6 border rounded-lg bg-white hover:scale-110 transition transform duration-300 ease-in w-fit" v-for="chat in chats" :key="chat.id">
            <router-link :to="{name:'Chat', params:{id: chat.id}}">
                <h1 class="font-bold text-[24px]">{{ chat.nombre }}</h1>
            </router-link>
        </div>
    </div>
    <div class="flex flex-col items-center justify-center">
        
        <router-link to="/create/chat">
            <BaseButton color="#CF3F25">Crear Chat</BaseButton>
        </router-link>
    </div>
</template>
<style>
.electric-button::before{
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(120deg, transparent 40%, rgba(0, 255, 255, 0.6), transparent 60%);
    transform: translateX(-100%);
    animation: lightning 2s infinite;
}

@keyframes lightning {
    0% { transform: translateX(-100%)}
    50% { transform: translateX(100%)}
    100% { transform: translateX(100%)}
}

.electric-button{
    position: relative;
    overflow: hidden;
}

@keyframes materialize {
    0% {
    opacity: 0;
    transform: scale(0.6) rotate(-10deg);
    filter: blur(10px);
  }
  60% {
    opacity: 1;
    transform: scale(1.05) rotate(2deg);
    filter: blur(0px);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }

}

@keyframes robotFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.energy-box {
  animation: materialize 0.4s ease-out forwards;
}

.robot-avatar {
  animation: robotFloat 2s ease-in-out infinite;
}
</style>