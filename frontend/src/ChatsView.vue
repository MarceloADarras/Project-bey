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

    <div class="relative z-10 min-h-[calc(100vh-64px)] p-6 max-w-5xl mx-auto flex flex-col justify-between">
        <!-- Floating Bot Toggle Button -->
        <div class="flex justify-end mb-4">
            <button 
                @click="chatOpen = !chatOpen" 
                class="w-14 h-14 flex items-center justify-center text-2xl bg-gradient-to-r from-amber-500 to-orange-600 rounded-2xl shadow-xl hover:scale-105 transition-all text-white border border-white/40 cursor-pointer z-20 boton-beybot"
                title="Abrir BeyBot"
            >
                🤖
            </button>
        </div>

        <!-- Chat Bot Window Overlay -->
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
                class="glass-card fixed bottom-24 right-6 w-80 h-96 rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden text-slate-900 dark:text-slate-100 border border-white/40 dark:border-slate-700/60"
            >
                <div class="bg-gradient-to-r from-amber-500 to-orange-600 text-white p-3 flex justify-between items-center shadow-md">
                    <div class="flex items-center gap-2 cursor-pointer" @click="showInfo = !showInfo">
                        <span class="text-2xl">🤖</span>
                        <span class="font-bold text-sm">BeyBot</span>
                    </div>
                    <button @click="chatOpen = false" class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-black/20 transition-colors">✕</button>
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
                        class="absolute top-14 right-4 bg-white/95 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-xs p-3 rounded-xl border border-slate-200 dark:border-slate-700 shadow-xl w-60 z-10"
                    >
                        ⚡ Soy BeyBot, tu asistente de BeyStory.
                        Puedo ayudarte a buscar beyblades, explicar piezas
                        y guiarte en tus batallas.
                    </div>
                </transition>

                <div class="flex-1 p-3 overflow-y-auto text-sm space-y-3">
                    <p v-if="mensajes.length === 0" class="text-slate-500 dark:text-slate-400 text-center py-4">Bienvenido Blader ⚡</p>
                    <div v-for="(m, index) in mensajes" :key="index">
                        <div v-if="m.role === 'user'" class="flex justify-end">
                            <div class="px-3 py-2 rounded-xl bg-orange-500 text-white max-w-[80%] text-xs shadow-sm">
                                <p>{{ m.text }}</p>
                            </div>
                        </div>
                        <div v-else class="flex justify-start">
                            <div class="px-3 py-2 rounded-xl bg-white/90 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 max-w-[80%] text-xs shadow-sm">
                                <p>{{ m.text }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-3 border-t border-slate-200/80 dark:border-slate-700 flex gap-2 bg-white/60 dark:bg-slate-900/60">
                    <input type="text" placeholder="Escribe un mensaje..." class="flex-1 bg-white/90 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-amber-500 shadow-inner" v-model="mensaje" @keyup.enter="enviarMensaje">
                    <button class="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-3 py-1.5 rounded-xl hover:opacity-90 transition-opacity text-xs font-semibold shadow-sm cursor-pointer" @click="enviarMensaje()">➤</button>
                </div>
            </div>
        </transition>

        <!-- Chats List Container -->
        <div class="flex-1 my-4">
            <div v-if="chats.length === 0" class="glass-card text-center p-8 rounded-2xl max-w-md mx-auto my-8 shadow-xl">
                <h2 class="text-xl font-bold mb-2 text-slate-900 dark:text-slate-100">No tienes chats creados</h2>
                <p class="text-sm text-slate-600 dark:text-slate-300">¡Crea tu primer chat para hablar con otros bladers!</p>
            </div>

            <div v-else class="flex flex-wrap items-center justify-center gap-6 py-4">
                <div class="glass-card flex flex-col justify-center p-6 rounded-2xl hover:border-amber-500 hover:-translate-y-1 transition-all duration-200 w-64 shadow-xl text-slate-900 dark:text-slate-100" v-for="chat in chats" :key="chat.id">
                    <router-link :to="{name:'Chat', params:{id: chat.id}}" class="no-underline">
                        <h1 class="font-bold text-xl text-slate-900 dark:text-slate-100 text-center hover:text-orange-600 dark:hover:text-amber-400 transition-colors">{{ chat.nombre }}</h1>
                    </router-link>
                </div>
            </div>
        </div>

        <!-- Create Chat Button Footer -->
        <div class="flex flex-col items-center justify-center mt-6 pb-6 z-10">
            <router-link to="/create/chat">
                <BaseButton color="#FF6B35" hoverColor="#E63946">Crear Chat</BaseButton>
            </router-link>
        </div>
    </div>
</template>



<style scoped>
    .boton-beybot {
        position: relative;
        overflow: hidden;
    }

    .boton-beybot::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            135deg,
            transparent 35%,
            rgba(255, 255, 255, 0.85) 50%,
            transparent 65%
        );
        transform: translate(-120%, -120%) rotate(25deg);
        animation: shine 3s infinite ease-in-out;
        pointer-events: none;
    }

    @keyframes shine {
        0% {
            transform: translate(-120%, -120%) rotate(25deg);
        }
        35% {
            transform: translate(120%, 120%) rotate(25deg);
        }
        100% {
            transform: translate(120%, 120%) rotate(25deg);
        }
    }
</style>

