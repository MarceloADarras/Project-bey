<script setup>
import api from './main';
import BaseButton from '../components/BaseButton.vue';
import Header from '../components/HeaderComponent.vue';
import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const router = useRoute()
const chat_id = router.params.id
const chatContent = ref(null);
const mensajeInput = ref("");

const modalEliminar = ref(false)

const user = localStorage.getItem("user")

const userInfo = JSON.parse(user)

const userNombre = userInfo.username

const cargarChat = async() => {
    try{
        const res = await api.get(`cargar/chat/${chat_id}`)
        chatContent.value = res.data
        console.log(chatContent.value)
    }catch(error){
        console.error(error)
    }
}

const enviarMensaje = async() => {
    if (!mensajeInput.value.trim()) return;
    
    try{
        await api.post("crear/mensaje", {
            id_chat: parseInt(chat_id),
            texto: mensajeInput.value
        })
        console.log("Mensaje enviado correctamente")
        mensajeInput.value = ""
        await cargarChat()
    }catch(error){
        console.error(error)
    }
}

const abrirEliminar = async() => {
    modalEliminar.value = true;
}

const cerrarModal = async() => {
    modalEliminar.value = false;
}

const eliminarChat = async() => {
    try{
        await api.delete(`eliminar/chat/${chat_id}`)
        console.log("Chat eliminado correctamente")
    }catch(error){
        console.error(error)
    }
}

onMounted(() => {
    cargarChat()
})
</script>
<template>
    <div class="flex flex-col h-screen overflow-hidden text-slate-900">
        <Header></Header>
        
        <!-- Chat Header -->
        <div class="glass-card p-4 flex-shrink-0 border-b border-slate-200">
            <div class="flex items-center justify-between max-w-5xl mx-auto">
                <div>
                    <h1 class="text-xl font-bold text-slate-900">{{ chatContent?.nombre || 'Chat' }}</h1>
                    <div class="text-xs text-slate-600 mt-1">
                        Participantes: {{ chatContent?.usuarios?.map(u => u.username).join(', ') || '' }}
                    </div>
                </div>
                <button @click="abrirEliminar()" class="px-4 py-2 bg-red-500 hover:bg-red-600 rounded-xl transition-colors text-white text-xs font-semibold shadow-sm">Eliminar Chat</button>
            </div>
        </div>

        <!-- Messages Container -->
        <div class="flex-1 overflow-y-auto p-4 max-w-5xl mx-auto w-full space-y-4">
            <div v-if="!chatContent" class="text-center text-slate-500 py-8">
                Cargando chat...
            </div>
            <div v-else-if="!chatContent.mensajes || chatContent.mensajes.length === 0" class="glass-card text-center font-medium text-slate-600 py-8 rounded-2xl">
                No hay mensajes en este chat
            </div>
            <div v-else class="flex flex-col space-y-3">
                <div 
                    v-for="mensajeItem in chatContent.mensajes" 
                    :key="mensajeItem.id"
                    class="flex"
                    :class="mensajeItem.usuario === userNombre ? 'justify-end' : 'justify-start'"
                >
                    <div 
                        class="max-w-xs lg:max-w-md px-4 py-2.5 rounded-2xl shadow-sm text-xs"
                        :class="mensajeItem.usuario === userNombre
                            ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-br-none' 
                            : 'glass-card text-slate-900 rounded-bl-none'"
                    >
                        <div class="font-semibold opacity-90 mb-1">
                            {{ mensajeItem.usuario }}
                        </div>
                        <div v-if="mensajeItem.texto" class="text-sm">
                            {{ mensajeItem.texto }}
                        </div>
                        <div v-if="mensajeItem.enlace" class="text-xs mt-1 underline">
                            <a :href="mensajeItem.enlace" target="_blank">{{ mensajeItem.enlace }}</a>
                        </div>
                        <div v-if="mensajeItem.archivo" class="text-xs mt-1">
                            📎 Archivo adjunto
                        </div>
                        <div class="text-[10px] opacity-75 mt-1 text-right">
                            {{ new Date(mensajeItem.created_at).toLocaleTimeString() }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Message Input -->
        <div class="glass-card p-4 flex-shrink-0 border-t border-slate-200">
            <div class="flex items-center space-x-3 max-w-5xl mx-auto">
                <input 
                    class="flex-1 px-4 py-2.5 bg-white/90 border border-slate-300 rounded-xl focus:outline-none focus:border-amber-500 text-slate-900 text-sm shadow-inner" 
                    placeholder="Escribe un mensaje..." 
                    v-model="mensajeInput"
                    type="text"
                    @keyup.enter="enviarMensaje()"
                >
                <button @click="enviarMensaje()" class="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-orange-600 text-white font-semibold rounded-xl hover:opacity-90 transition-opacity text-sm shadow-md">
                    Enviar
                </button>
            </div>
        </div>
    </div>
    <ModalEliminarComponent v-if="modalEliminar" :texto="'¿Desea Eliminar el chat?'" :texto-boton="'Eliminar'" :texto-boton2="'Cancelar'" color="#E63946" @cancelar="cerrarModal()" @eliminar="eliminarChat()"></ModalEliminarComponent>
</template>
