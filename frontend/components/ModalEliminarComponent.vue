<script setup>
import BaseButton from './BaseButton.vue';
const props = defineProps({
    texto: String,
    textoBoton: String,
    textoBoton2: String,
    color: String,
    hoverColor: String
})

const emit = defineEmits(['cancelar', 'eliminar'])

</script>

<template>
    <div class="fixed inset-0 w-screen h-screen bg-black/40 backdrop-blur-sm flex items-center justify-center z-[9999] p-4">
        <div class="glass-card flex flex-col items-center justify-center max-w-md w-full p-8 rounded-2xl gap-5 shadow-2xl text-slate-900 text-center">
            <h1 class="text-lg font-medium text-slate-800">{{ texto }}</h1>
            <div class="flex items-center justify-center gap-4 mt-2">
                <BaseButton :color="color || '#E63946'" :hover-color="hoverColor || '#B71C1C'" @click="emit('eliminar')">{{ textoBoton }}</BaseButton>
                <BaseButton color="#64748B" hoverColor="#475569" @click="emit('cancelar')">{{ textoBoton2 }}</BaseButton>
            </div>
        </div>
    </div>
</template>


