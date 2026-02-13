<script setup>
    import api from './main';
    import { ref, watch, computed } from 'vue';
    import Header from '../components/HeaderComponent.vue'
    import CreateComponent from '../components/CreateComponent.vue';
    import { useRoute } from 'vue-router';

    const route = useRoute();

    // Make eleccion reactive to route changes
    const eleccion = computed(() => route.params.nombre);

    // Format the title for better display
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

    const creacion = ref("bey")

    const crearElemento = async(data)=>{
        try {
            let response;
            
            if (data instanceof FormData) {
                // Handle FormData (beyblade with image)
                console.log('Enviando FormData para beyblade:', data);
                response = await api.post("crear/beyblade", data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            } else {
                // Handle JSON data (other components)
                switch(data.tipo){
                    case 'fusion':
                        console.log('Enviando JSON para fusion:', data);
                        response = await api.post("crear/fusion", data)
                        break
                    case 'clear':
                        console.log('Enviando JSON para clear:', data);
                        response = await api.post("crear/clear", data)
                        break
                    case 'track':
                        console.log('Enviando JSON para track:', data);
                        response = await api.post("crear/track", data)
                        break
                    case 'tip':
                        console.log('Enviando JSON para tip:', data);
                        response = await api.post("crear/tip", data)
                        break
                    case 'tipe':
                        console.log('Enviando JSON para tipe:', data);
                        response = await api.post("crear/tipe", data)
                        break
                }
            }
            
            console.log('Respuesta del servidor:', response.data);
            
            // Show success message and potentially redirect
            alert('Elemento creado exitosamente!');
            
        } catch (error) {
            console.error('Error al crear elemento:', error);
            alert('Error al crear el elemento: ' + (error.response?.data?.error || error.message));
        }
    }

</script>

<template>

    <Header></Header>
    <div class="flex justify-center">
        <div class="relative gap-4 p-6 m-6 border-1 rounded-lg bg-white w-fit ">
            <h1 class="text-black text-[24px] font-bold italic">Crear {{ tituloFormateado }}</h1>
        </div>
    </div>

    <div class="flex items-center justify-center">
        <CreateComponent
            :eleccion="eleccion"
            @creation-info="crearElemento"
        ></CreateComponent>
    </div>

    
</template>