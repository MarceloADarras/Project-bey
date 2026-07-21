<script setup>
import Header from '../components/HeaderComponent.vue'
import { useTheme } from './theme'

const { theme, setTheme } = useTheme()
</script>

<template>
    <Header></Header>
    <div class="flex flex-col items-center justify-center p-6 max-w-4xl mx-auto min-h-[calc(100vh-64px)]">
        <div class="glass-card w-full p-8 rounded-2xl shadow-xl flex flex-col items-center gap-6">
            <div class="text-center">
                <h1 class="text-3xl font-bold mb-2">⚙️ Configuración / Settings</h1>
                <p class="text-sm opacity-80">Personaliza la apariencia y el tema visual de la aplicación BeyStory.</p>
            </div>

            <div class="w-full max-w-lg space-y-4 mt-2">
                <h2 class="text-lg font-semibold border-b pb-2 border-slate-500/30">Selección de Tema</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Light Theme Option -->
                    <button 
                        @click="setTheme('light')" 
                        type="button" 
                        class="flex flex-col items-center justify-center p-6 rounded-2xl border-2 transition-all cursor-pointer gap-3 text-center"
                        :class="theme === 'light' ? 'border-amber-500 bg-amber-500/10 shadow-lg scale-105' : 'border-slate-300/40 hover:border-amber-400 bg-white/40'"
                    >
                        <span class="text-4xl">☀️</span>
                        <div>
                            <h3 class="font-bold text-lg">Modo Claro</h3>
                            <p class="text-xs opacity-75 mt-1">Fondo brillante porcelana con resplandores cálidos.</p>
                        </div>
                        <span v-if="theme === 'light'" class="text-xs font-semibold px-3 py-1 bg-amber-500 text-white rounded-full mt-1">Activo</span>
                    </button>

                    <!-- Dark Theme Option -->
                    <button 
                        @click="setTheme('dark')" 
                        type="button" 
                        class="flex flex-col items-center justify-center p-6 rounded-2xl border-2 transition-all cursor-pointer gap-3 text-center"
                        :class="theme === 'dark' ? 'border-amber-500 bg-amber-500/10 shadow-lg scale-105' : 'border-slate-300/40 hover:border-amber-400 bg-slate-900/40'"
                    >
                        <span class="text-4xl">🌙</span>
                        <div>
                            <h3 class="font-bold text-lg">Modo Oscuro</h3>
                            <p class="text-xs opacity-75 mt-1">Fondo neón nocturno con auroras y mallas de color.</p>
                        </div>
                        <span v-if="theme === 'dark'" class="text-xs font-semibold px-3 py-1 bg-amber-500 text-white rounded-full mt-1">Activo</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
