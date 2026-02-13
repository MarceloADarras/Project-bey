<script setup>
import { ref } from 'vue';
const props = defineProps({
    texto: String,
    color: String,
    hoverColor: {
        type: String,
        default: 'blue'
    }
})

const isHover = ref(false)

const emit = defineEmits(['accion'])
</script>
<template>
    <button type="button" class="px-4 py-2 w-[100px] font-bold border-2 border-black rounded-lg border-w-[2px] transition-all duration-300 hover:scale-110" :style="{backgroundColor: isHover ? hoverColor : color}" @mouseenter="isHover = true" @mouseleave="isHover = false" @click="emit('accion', $event)"><slot></slot></button>
</template>
<style>
    .boton{
        padding: 1%;
        width: 100px;
        border: 1px solid black;
        border-radius: 20%;
        border-width: 2px;
        transition: all 0.3s ease;
    }

    .boton:hover{
        background-color: blue;
    }
</style>