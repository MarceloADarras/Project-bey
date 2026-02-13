<script setup>
    import { ref, onMounted } from 'vue';
    import api from './main';
    import BeyComponent from '../components/BeyComponent.vue';
    import Header from '../components/HeaderComponent.vue'
    import BaseButton from '../components/BaseButton.vue';
    import { RouterLink } from 'vue-router';

    const beyblades = ref([])

    const busqueda = ref("")

    const user = localStorage.getItem('user')
    const token = localStorage.getItem('auth_token')

    const cargarBeys =  async() => {
        const res = await api.get("cargar/beyblade")
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

    onMounted(() => {
        cargarBeys()
    })
</script>

<template>
    <Header></Header>


        <div v-if="user && token">
            <div class="flex justify-center p-6">
                <div class="flex justify-center gap-2 bg-white w-fit rounded-lg">
                    <h1 class="font-bold text-[24px]">Busca algun beyblade</h1>
                </div>
            </div>
            <div class="flex justify-center gap-4">
                
                <form @submit.prevent = "buscar">
                    <input type="text" v-model="busqueda" class="w-[300px] h-[40px] border-2 border-black rounded-lg">
                    <button class="bg-blue-500 rounded-lg px-4 py-2 m-6 hover:scale-110 transition transform duration-100 ease-in">Buscar</button>
                </form>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6 max-w-7xl mx-auto">
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

    .link{
        text-decoration: none;
        color: black;
    }
</style>