<script setup>
defineProps({
    cargando: {
        type: Boolean,
        default: false
    },
    mensaje: {
        type: String,
        default: 'Cargando...'
    }
})
</script>

<template>
    <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
    >
        <div v-if="cargando" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-md p-4">
            <div class="glass-card flex flex-col items-center justify-center p-8 rounded-3xl shadow-2xl max-w-sm w-full text-center gap-6 border border-white/20">
                <!-- Beyblade Spin Loading Animation -->
                <div class="relative flex items-center justify-center w-24 h-24">
                    <div class="absolute inset-0 rounded-full border-4 border-t-amber-500 border-r-orange-600 border-b-red-600 border-l-transparent animate-spin"></div>
                    <div class="absolute inset-2 rounded-full border-4 border-t-transparent border-r-amber-400 border-b-orange-500 border-l-red-500 animate-spin" style="animation-direction: reverse; animation-duration: 0.8s;"></div>
                    <span class="text-3xl animate-bounce">🌀</span>
                </div>

                <div class="space-y-1">
                    <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100">{{ mensaje }}</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Por favor espera un momento...</p>
                </div>
            </div>
        </div>
    </transition>
</template>

<style scoped>
</style>
