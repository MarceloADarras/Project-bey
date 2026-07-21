<script setup>
    import { ref, onMounted, watch, computed } from 'vue';
    import api from './main';
    import BeyComponent from '../components/BeyComponent.vue';
    import Header from '../components/HeaderComponent.vue'
    import BaseButton from '../components/BaseButton.vue';
    import { RouterLink } from 'vue-router';
    import { useRoute } from 'vue-router';

    const route = useRoute()

    const seleccion = computed(() => route.params.season)

    const beyblades = ref([])

    const busqueda = ref("")


    const user = localStorage.getItem('user')
    const token = localStorage.getItem('auth_token')

    const cargarBeys =  async(select) => {
        const params = {}
        if (select && select.value) {
            params.select = select.value
            seleccion.value = select.value
        } else {
            seleccion.value = ""
        }
        const res = await api.get("cargar/beyblade", {
            params: params
        })
        beyblades.value = res.data
        console.log(beyblades.value)
    }

    const buscar = async() => {
        if(!busqueda.value.trim()){
            await cargarBeys()
            return
        }
        try{
            const res = await api.get("buscador", {
                params: {
                    busqueda: busqueda.value
                }
            })

            beyblades.value = res.data
            
        }catch(error){
            console.error(error)
        }
    }

    watch(
        () => route.params.season,
        (newSeason) => {
            if(newSeason) {
                seleccion.value = newSeason
                cargarBeys({value: newSeason})
            } else {
                seleccion.value = ""
                beyblades.value = []
            }
        },
        {inmediate: true}
    )

    onMounted(() => {
        if(route.params.season){
            seleccion.value = route.params.season
            cargarBeys({value: route.params.season})
        } else if(route.params.season === "Home"){
            seleccion.value = "Main"
        }
    })
</script>

<template>
    <Header></Header>

    <div v-if="user && token" class="min-h-[calc(100vh-64px)] p-6">
        <div v-if="!seleccion" class="flex flex-col justify-center items-center py-12 gap-8 max-w-5xl mx-auto">
            <div class="glass-card text-slate-900 dark:text-slate-100 font-bold text-2xl px-8 py-4 rounded-2xl">
                <h1>Selecciona una temporada</h1>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl px-4">
                <router-link :to="{name: 'Home', params:{season: 'Fusion'}}" class="group">
                    <div class="glass-card rounded-2xl p-2 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden">
                        <img class="w-full h-48 object-cover rounded-xl" :src="'/img/Beyblade_metal_fusion.webp'" alt="Metal Fusion">
                    </div>
                </router-link>

                <router-link :to="{name: 'Home', params:{season: 'Masters'}}" class="group">
                    <div class="glass-card rounded-2xl p-2 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden">
                        <img class="w-full h-48 object-cover rounded-xl" :src="'/img/Beyblade_metal_masters.webp'" alt="Metal Masters">
                    </div>
                </router-link>

                <router-link :to="{name: 'Home', params:{season: 'Fury'}}" class="group">
                    <div class="glass-card rounded-2xl p-2 group-hover:border-amber-500 group-hover:scale-105 transition-all duration-300 overflow-hidden">
                        <img class="w-full h-48 object-cover rounded-xl" :src="'/img/Beyblade_Metal_Fury.png'" alt="Metal Fury">
                    </div>
                </router-link>
            </div>

            <div class="flex justify-center mt-4">
                <div class="glass-card px-6 py-3 rounded-xl">
                    <p class="text-lg font-semibold text-orange-600 dark:text-amber-400 text-center">Más temporadas pronto...</p>
                </div>
            </div>
        </div>

        <div v-if="seleccion" class="max-w-7xl mx-auto">
            <div>
                <div class="flex justify-center p-4">
                    <div class="flex items-center gap-3 glass-card px-6 py-3 rounded-2xl">
                        <h1 class="font-bold text-2xl text-slate-900 dark:text-slate-100">{{ seleccion }}</h1>
                        <button @click="$router.push({name: 'Home'})" class="ml-3 bg-red-500 hover:bg-red-600 text-white w-7 h-7 flex items-center justify-center rounded-lg text-sm transition-colors shadow-sm">✕</button>
                    </div>
                </div>
                
                <div class="flex justify-center my-4">
                    <form @submit.prevent="buscar" class="flex items-center gap-3 glass-card p-2 rounded-2xl">
                        <input type="text" v-model="busqueda" placeholder="Buscar Beyblade..." class="w-64 md:w-80 px-4 py-2 bg-white/90 dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded-xl focus:outline-none focus:border-amber-500 transition-colors shadow-inner">
                        <button class="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold rounded-xl px-5 py-2 transition-all shadow-md">Buscar</button>
                    </form>
                </div>
            </div>

            <div v-if="beyblades.length != 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6 max-w-7xl mx-auto">
                <div v-for="bey in beyblades" :key="bey.id" class="glass-card flex justify-center p-3 rounded-2xl transition-all duration-300 hover:-translate-y-1 hover:border-amber-500 overflow-hidden">
                    <router-link class="no-underline text-slate-900 dark:text-slate-100 w-full" :to="{name: 'Ver', params:{id : bey.id}}" >
                        <BeyComponent
                            :photo="bey.photo"
                            :nombre="bey.nombre"
                            :color="bey.color"
                            :compact="true"
                        />
                    </router-link>
                </div>
            </div>
        </div>

        <div v-if="seleccion === 'Main'" class="flex justify-center p-6">
            <div class="glass-card flex flex-col items-center justify-center gap-4 p-6 rounded-2xl text-slate-900 dark:text-slate-100">
                <h1 class="text-xl font-bold">¡NO HAY BEYBLADES CREADOS!</h1>
                <p class="text-slate-600 dark:text-slate-300">Añade beyblades ahora</p>
                <router-link to="/create/bey">
                    <button class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 text-white font-semibold hover:opacity-90 transition-opacity shadow-md">Añadir beyblades</button>
                </router-link>
            </div>
        </div>
    </div>

    <div class="relative min-h-[calc(100vh-64px)] flex items-center justify-center p-6" v-else>
        <div class="glass-card relative flex flex-col items-center text-center max-w-md p-8 rounded-2xl gap-4">
            <h1 class="font-bold text-slate-900 dark:text-slate-100 text-2xl mb-2">Inicia sesión para conectar con otros bladers</h1>
            <router-link to="/iniciar">
                <BaseButton color="#FF6B35" hoverColor="#E63946">Iniciar Sesión</BaseButton>
            </router-link>
            <div class="mt-2 text-xs text-slate-600 dark:text-slate-400">
                <p>
                    ¿No estás registrado? 
                    <router-link to="/registro" class="text-orange-600 dark:text-amber-400 hover:text-red-600 dark:hover:text-amber-300 font-semibold underline ml-1">Regístrate aquí</router-link>
                    y únete a BeyStory
                </p>
            </div>
        </div>
    </div>
</template>




<style scoped>
    .link {
        text-decoration: none;
    }
</style>