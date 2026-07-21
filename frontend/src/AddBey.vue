<script setup>
    import api from './main';
    import { ref, computed } from 'vue';
    import Header from '../components/HeaderComponent.vue'
    import CreateComponent from '../components/CreateComponent.vue';
    import LoadingOverlay from '../components/LoadingOverlay.vue';
    import { useRoute, useRouter } from 'vue-router';

    const route = useRoute();
    const router = useRouter();

    const eleccion = computed(() => route.params.nombre);

    const tituloFormateado = computed(() => {
        const item = eleccion.value;
        if (!item) return 'Crear';
        
        const titles = {
            'bey': 'Beyblade',
            'fusion': 'Fusion Wheel',
            'clear': 'Clear Wheel', 
            'track': 'Spin Track',
            'tip': 'Tip',
            'tipe': 'Type'
        };
        
        return titles[item] || item.charAt(0).toUpperCase() + item.slice(1);
    });

    const cargando = ref(false);
    const mensajeCarga = ref('Creando elemento...');

    const crearElemento = async(data)=>{
        try {
            cargando.value = true;
            mensajeCarga.value = `Guardando ${tituloFormateado.value}...`;

            let response;
            
            if (data instanceof FormData) {
                console.log('Enviando FormData para beyblade:', data);
                response = await api.post("crear/beyblade", data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            } else {
                switch(data.tipo){
                    case 'fusion':
                    case 'clear':
                    case 'track':
                    case 'tip':
                    case 'tipe':
                        console.log('Enviando JSON para pieza:', data);
                        response = await api.post("crear/pieza", data);
                        break;
                }
            }
            
            console.log('Respuesta del servidor:', response?.data);
            mensajeCarga.value = `¡${tituloFormateado.value} creado exitosamente! Redirigiendo...`;
            
            setTimeout(() => {
                cargando.value = false;
                router.push('/home');
            }, 1000);
            
        } catch (error) {
            cargando.value = false;
            console.error('Error al crear elemento:', error);
            alert('Error al crear el elemento: ' + (error.response?.data?.error || error.response?.data?.detail || error.message));
        }
    }

</script>

<template>
    <Header></Header>
    <LoadingOverlay :cargando="cargando" :mensaje="mensajeCarga" />

    <div class="flex flex-col items-center justify-center p-6 max-w-4xl mx-auto min-h-[calc(100vh-64px)]">
        <div class="glass-card p-6 rounded-2xl shadow-xl w-full mb-6 text-center">
            <h1 class="text-slate-900 dark:text-slate-100 text-2xl font-bold">Crear {{ tituloFormateado }}</h1>
        </div>

        <div class="w-full flex justify-center">
            <CreateComponent
                :eleccion="eleccion"
                @creation-info="crearElemento"
            ></CreateComponent>
        </div>
    </div>
</template>

