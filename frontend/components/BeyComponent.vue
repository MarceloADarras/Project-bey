<script setup>
    import { computed } from 'vue'
    
    const prop = defineProps({
        photo: String, // Changed from foto to photo to match backend
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
        compact: {type: Boolean, default: false} // New prop for Home view
    })

    // Computed property to check if we should show component details
    const showDetails = computed(() => {
        return prop.fusion || prop.clear || prop.track || prop.tip || prop.tipe
    })
</script>

<template>
    <div :style="{backgroundColor: color}">
        <!-- Main info - always shown -->
        <div class="flex items-center justify-center font-sans p-6 bg-white text-black" :class="{'border-2 border-black': !compact}">
            <img 
                v-if="photo"
                :src="photo ? `http://127.0.0.1:8000${photo}` : ''" 
                class="w-24 h-auto mr-6"
            >
            <div class="max-w-md text-center">
                
                <h3 class="font-sans font-semibold text-3xl mb-4 text-black">{{prop.nombre}}</h3>
                <h4 v-if="prop.descripcion" class="font-sans text-base">{{ prop.descripcion }}</h4>
            </div>
        </div>
        
        <!-- Component details - only shown if props exist -->
        <div v-if="showDetails" class="mt-5 px-2.5">
            <div v-if="prop.fusion" class="mb-3.5 p-2.5 rounded-lg bg-white/5 border-l-4 border-[#FF6B35]">
                <h3 class="font-sans font-semibold underline text-black">{{prop.fusion}}</h3>
                <h4 class="font-sans text-base text-black">{{ prop.descripcion1 }}</h4>
            </div>
            <div v-if="prop.clear" class="mb-3.5 p-2.5 rounded-lg bg-white/5 border-l-4 border-[#FF6B35]">
                <h3 class="font-sans font-semibold underline text-black">{{prop.clear}}</h3>
                <h4 class="font-sans text-base text-black">{{ prop.descripcion2 }}</h4>
            </div>
            <div v-if="prop.track" class="mb-3.5 p-2.5 rounded-lg bg-white/5 border-l-4 border-[#FF6B35]">
                <h3 class="font-sans font-semibold underline text-black">{{prop.track}}</h3>
                <h4 class="font-sans text-base text-black">{{ prop.descripcion3 }}</h4>
            </div>
            <div v-if="prop.tip" class="mb-3.5 p-2.5 rounded-lg bg-white/5 border-l-4 border-[#FF6B35]">
                <h3 class="font-sans font-semibold underline text-black">{{prop.tip}}</h3>
                <h4 class="font-sans text-base text-black">{{ prop.descripcion4 }}</h4>
            </div>
            <div v-if="prop.tipe" class="mb-3.5 p-2.5 rounded-lg bg-white/5 border-l-4 border-[#FF6B35]">
                <h3 class="font-sans font-semibold underline text-black">{{prop.tipe}}</h3>
                <h4 class="font-sans text-base text-black">{{ prop.descripcion5 }}</h4>
            </div>
        </div>
    </div>
</template>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
</style>