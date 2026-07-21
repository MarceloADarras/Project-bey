<script setup>
import BaseButton from './BaseButton.vue';

const props = defineProps({
    titulo: String,
    detalle: String
})

const emit = defineEmits(['cerrar'])
</script>
<template>
    <div class="modal-overlay" @click.self="emit('cerrar')">
        <div class="glass-card flex flex-col items-center justify-center font-sans rounded-2xl p-8 m-4 gap-5 max-w-md w-full shadow-2xl text-slate-900">
            <h1 class="font-bold text-2xl text-orange-600 text-center">{{ titulo }}</h1>
            <h3 class="text-slate-700 text-center text-sm leading-relaxed">{{ detalle }}</h3>
            <div class="mt-2">
                <BaseButton color="#FF6B35" hoverColor="#E63946" @click="emit('cerrar')">Cerrar</BaseButton>
            </div>
        </div>
    </div>
</template>


<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}
</style>