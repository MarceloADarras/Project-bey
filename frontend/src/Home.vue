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


        <div v-if="user && token">
            <div v-if="!seleccion" class="flex flex-col justify-center items-center min-h-screen gap-6">

                <div class="border-2 border-black bg-white text-black font-bold text-[24px] px-6 py-2 rounded-lg">
                    <h1>Selecciona una temporada</h1>
                </div>

                <div class="flex gap-4">
                    <router-link :to="{name: 'Home', params:{season: 'Fusion'}}">
                        <div
                            class="flex justify-center border-2 border-black w-fit h-[200px] rounded-lg hover:scale-110 transition-all duration-200">
                            <img class="w-[400px] h-auto rounded-lg" :src="'/img/Beyblade_metal_fusion.webp'" alt="">
                        </div>
                    </router-link>

                    <router-link :to="{name: 'Home', params:{season: 'Masters'}}">
                        <div
                            class="flex justify-center border-2 border-black w-fit h-[200px] rounded-lg hover:scale-110 transition-all duration-200">
                            <img class="w-[400px] h-auto rounded-lg" :src="'/img/Beyblade_metal_masters.webp'" alt="">
                        </div>
                    </router-link>

                    <router-link :to="{name: 'Home', params:{season: 'Fury'}}">
                        <div
                            class="flex justify-center border-2 border-black w-fit h-[200px] rounded-lg hover:scale-110 transition-all duration-200">
                            <img class="w-[400px] h-auto rounded-lg" :src="'/img/Beyblade_Metal_Fury.png'" alt="">
                        </div>
                    </router-link>
                </div>


                <div class="flex justify-center">
                    <div class="border rounded-lg bg-white mt-10 w-fit">
                        <p class="rainbow-text text-2xl font-bold text-center">Más temporadas pronto...</p>
                    </div>
                </div>

            </div>
            <div v-if="seleccion">
                <div>
                    <div class="flex justify-center p-6">
                        <div class="flex justify-center gap-2 bg-white w-fit rounded-lg">
                            <h1 class="font-bold text-[24px]">{{ seleccion }}</h1>
                            <button @click="$router.push({name: 'Home'})" class="ml-4 bg-red-500 text-white px-2 rounded">X</button>
                        </div>
                    </div>
                    <div class="flex justify-center gap-4">
                        
                        <form @submit.prevent = "buscar">
                            <input type="text" v-model="busqueda" class="w-[300px] h-[40px] border-2 border-black rounded-lg">
                            <button class="bg-blue-500 rounded-lg px-4 py-2 m-6 hover:scale-110 transition transform duration-100 ease-in">Buscar</button>
                        </form>
                    </div>
                </div>
                <div v-if="beyblades.length != 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6 max-w-7xl mx-auto">
                    <div v-for="bey in beyblades" :key="bey.id" class="flex justify-center p-4 border-2 border-black rounded-[20%] transition duration-300 hover:scale-110 bg-white text-black">
                        <router-link class="no-underline text-black" :to="{name: 'Ver', params:{id : bey.id}}" >
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
                <div class="flex flex-col items-center justify-center gap-4 px-4 py-2 border rounded-lg bg-white w-fit">
                    <h1>¡NO HAY BEYBLADES CREADOS!</h1>
                    <p>Añade beyblades ahora</p>
                    <router-link to="/create/bey">
                        <button class="px-4 py-2 border-2 border-black rounded-lg bg-blue-200 hover:scale-110 hover:bg-blue-500 transition-all transform duration-200">Añadir beyblades</button>
                    </router-link>
                </div>
            </div>
        </div>
        <div class="relative min-h-screen flex items-center justify-center" v-else>
            
            <div class="relative flex flex-col items-center text-center border-2 border-black bg-white max-w-md p-6 rounded-lg gap-2" >
                <h1 class="font-bold text-black text-[24px] mb-6 italic">Inicia sesión para conectar con otros bladers</h1>
                <router-link to="/iniciar">
                    <BaseButton color="#E88B3A">Iniciar Sesion</BaseButton>
                </router-link>
                <div class="gap-4">
                    <div class="bottom-2 right-6 text-[10px] text-gray-600 whitespace-nowrap gap-4">
                        <h3 >
                            ¿No estás registrado? 
                            <router-link to="/registro" class="text-blue-600 hover:text-red-500">Registrate aqui</router-link>
                            y unete a beystory
                        </h3>
                    </div>
                </div>
            </div>
        </div>

</template>

<style>

    @keyframes rainbow {
        0% { background-position: 0% 50%;}
        50% { background-position: 100% 50%;}
        100% { background-position: 0% 50%;}
    }

    .rainbow-text{
        background: linear-gradient(
            90deg,
            #ff0000,
            #ff7f00,
            #ffff00,
            #00ff00,
            #0000ff,
            #4b0082,
            #8f00ff
        );
        background-size: 400% 400%;
        animation: rainbow 6s ease infinite;
        -webkit-background-clip: text;  
        -webkit-text-fill-color: transparent;
    }

    .link{
        text-decoration: none;
        color: black;
    }
</style>