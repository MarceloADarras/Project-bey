<script setup>
import { ref } from 'vue';

const props = defineProps({
    texto: String,
    color: {
        type: String,
        default: '#FF6B35'
    },
    hoverColor: String
})

const isHover = ref(false)
const emit = defineEmits(['accion'])
</script>

<template>
    <button 
        type="button" 
        class="px-5 py-2.5 min-w-[110px] font-semibold text-white rounded-xl transition-all duration-200 shadow-md hover:shadow-lg active:scale-95 cursor-pointer text-sm" 
        :style="{ backgroundColor: (isHover && hoverColor) ? hoverColor : color }" 
        @mouseenter="isHover = true" 
        @mouseleave="isHover = false" 
        @click="emit('accion', $event)"
    >
        <slot></slot>
    </button>
</template>