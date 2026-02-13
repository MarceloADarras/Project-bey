<script setup>
import BaseButton from './BaseButton.vue';

const props = defineProps({
    titulo: String,
    detalle: String
})

const emit = defineEmits(['cerrar'])
</script>
<template>
    <div class="modal-overlay">
        <div class="flex flex-col items-center justify-center font-sans border-2 border-black rounded-lg p-6 m-10 gap-4 bg-white">
            <h1 class="font-bold text-3xl underline">{{ titulo }}</h1>
            <h3>{{ detalle }}</h3>
            <BaseButton :color="'Cyan'" :hover-color="'Red'" @click="emit('cerrar')">Cerrar</BaseButton>
        </div>
    </div>
</template>

<style>
.modal-overlay{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;

    background: rgba(0,0,0,0.5);

    display: flex;
    align-items: center;
    justify-content: center;

    z-index: 9999;
}

.modal{
    background: white;
    padding: 20px;
    border-radius: 12px;
    min-width: 300px;
}
</style>