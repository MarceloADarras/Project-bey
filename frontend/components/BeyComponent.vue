<script setup>
    import { computed } from 'vue'
    
    const prop = defineProps({
        photo: String,
        nombre: {String, required: true},
        descripcion: String,
        fusion: String,
        descripcion1: String,
        clear: String,
        descripcion2: String,
        track: String,
        descripcion3: String,
        tip: String,
        descripcion4: String,
        tipe: String,
        descripcion5: String,
        color: {String},
        compact: {type: Boolean, default: false}
    })

    const showDetails = computed(() => {
        return prop.fusion || prop.clear || prop.track || prop.tip || prop.tipe
    })
</script>

<template>
    <div class="rounded-xl overflow-hidden" :style="{ backgroundColor: color ? color + '20' : 'transparent' }">
        <!-- Main info -->
        <div class="flex items-center justify-center font-sans p-4 text-slate-900 dark:text-slate-100 bg-white/70 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-white/80 dark:border-slate-700/60 shadow-sm" :class="{'shadow-md': !compact}">
            <img 
                v-if="photo"
                :src="photo ? `https://project-bey-production.up.railway.app${photo}` : ''" 
                class="w-20 h-20 object-contain mr-4 rounded-lg"
            >
            <div class="max-w-md text-center">
                <h3 class="font-bold text-2xl mb-1 text-slate-900 dark:text-slate-100">{{prop.nombre}}</h3>
                <h4 v-if="prop.descripcion" class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion }}</h4>
            </div>
        </div>
        
        <!-- Component details -->
        <div v-if="showDetails" class="mt-4 space-y-2 px-2">
            <div v-if="prop.fusion" class="p-3 rounded-xl bg-white/80 dark:bg-slate-800/80 border-l-4 border-[#FF6B35] shadow-sm">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100">{{prop.fusion}}</h3>
                <h4 class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion1 }}</h4>
            </div>
            <div v-if="prop.clear" class="p-3 rounded-xl bg-white/80 dark:bg-slate-800/80 border-l-4 border-[#FF6B35] shadow-sm">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100">{{prop.clear}}</h3>
                <h4 class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion2 }}</h4>
            </div>
            <div v-if="prop.track" class="p-3 rounded-xl bg-white/80 dark:bg-slate-800/80 border-l-4 border-[#FF6B35] shadow-sm">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100">{{prop.track}}</h3>
                <h4 class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion3 }}</h4>
            </div>
            <div v-if="prop.tip" class="p-3 rounded-xl bg-white/80 dark:bg-slate-800/80 border-l-4 border-[#FF6B35] shadow-sm">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100">{{prop.tip}}</h3>
                <h4 class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion4 }}</h4>
            </div>
            <div v-if="prop.tipe" class="p-3 rounded-xl bg-white/80 dark:bg-slate-800/80 border-l-4 border-[#FF6B35] shadow-sm">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100">{{prop.tipe}}</h3>
                <h4 class="text-sm text-slate-600 dark:text-slate-300">{{ prop.descripcion5 }}</h4>
            </div>
        </div>
    </div>
</template>



<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
</style>