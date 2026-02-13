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
    <div class="fixed inset-0 w-screen h-screen bg-black/50 flex items-center justify-center z-[9999]">
        <div class="flex flex-col items-center justify-center max-w-auto bg-white p-6 border-2 border-black rounded-lg gap-2">
            <h1>{{ texto }}</h1>
            <div class="flex items-center justify-center gap-4">
                <BaseButton :color="color" :hover-color="hoverColor" @click="emit('eliminar')">{{ textoBoton }}</BaseButton>
                <BaseButton @click="emit('cancelar')">{{ textoBoton2 }}</BaseButton>
            </div>
        </div>
    </div>
</template>
