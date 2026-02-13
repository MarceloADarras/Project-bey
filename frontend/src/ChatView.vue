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
    <div class="flex flex-col h-screen">
        <Header></Header>
        
        <!-- Chat Header -->
        <div class="bg-gray-100 p-4 border-b flex-shrink-0">
            <div class="flex justify-end">
                <button @click="abrirEliminar()" class="px-6 py-2 bg-red-500 rounded-lg hover:bg-red-900 transition-colors text-white">Eliminar Chat</button>
            </div>
            <h1 class="text-xl font-bold">{{ chatContent?.nombre || 'Chat' }}</h1>
            <div class="text-sm text-gray-600">
                Participantes: {{ chatContent?.usuarios?.map(u => u.username).join(', ') || '' }}
            </div>
            
            
        </div>

        <!-- Messages Container -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4 pb-4 gap-4">
            <div v-if="!chatContent" class="text-center text-gray-500">
                Cargando chat...
            </div>
            <div v-else-if="!chatContent.mensajes || chatContent.mensajes.length === 0" class="text-center font-bold text-black bg-white">
                No hay mensajes en este chat
            </div>
            <div v-else class="flex flex-col space-y-4">
                <div 
                    v-for="mensajeItem in chatContent.mensajes" 
                    :key="mensajeItem.id"
                    class="flex"
                    :class="mensajeItem.usuario === userNombre ? 'justify-end' : 'justify-start'"
                >
                    <div 
                        class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
                        :class="mensajeItem.usuario === userNombre
                            ? ' bg-blue-500 text-white ' 
                            : 'bg-gray-200 text-gray-800'"
                    >
                        <div class="text-xs font-semibold mb-1">
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
                        <div class="text-xs opacity-75 mt-1">
                            {{ new Date(mensajeItem.created_at).toLocaleTimeString() }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Message Input - Always at bottom -->
        <div class="border-t p-4 bg-white flex-shrink-0">
            <div class="flex items-center space-x-2">
                <input 
                    class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    placeholder="Escribe un mensaje..." 
                    v-model="mensajeInput"
                    type="text"
                    @keyup.enter="enviarMensaje()"
                >
                <button @click="enviarMensaje()" class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                    Enviar
                </button>
            </div>
        </div>
    </div>
    <ModalEliminarComponent v-if="modalEliminar" :texto="'¿Desea Eliminar el chat?'" :texto-boton="'Eliminar'" :texto-boton2="'Cancelar'" color="red" @cancelar="cerrarModal()" @eliminar="eliminarChat()"></ModalEliminarComponent>
</template>