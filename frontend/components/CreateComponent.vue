<script setup>
    import { ref } from 'vue'
    import api from '@/main'
    import BaseButton from './BaseButton.vue'
    const nombre = ref("")
    const descripcion = ref("")
    const fusion_wheel = ref([])
    const clear_wheel = ref([])
    const track = ref([])
    const tip = ref([])
    const tipe = ref([])
    const image = ref()
    const color = ref("")

    const nombres = ref("")
    const descripciones = ref("")
    const fusionWheels = ref([])
    const clearWheels = ref([])
    const tracks = ref([])
    const tips = ref([])
    const tipes = ref([])
    const props=defineProps({
        eleccion: String,
    })

    const cargarOpciones = async() => {
        try{
            if(props.eleccion == "bey"){
                const fus = await api.get("cargar/fusion")
                const cle = await api.get("cargar/clear")
                const tra = await api.get("cargar/track")
                const pun = await api.get("cargar/tip")
                const tipo = await api.get("cargar/tipe")

                fusionWheels.value = fus.data
                clearWheels.value = cle.data
                tracks.value = tra.data
                tips.value = pun.data
                tipes.value = tipo.data
            }
            console.log(fusion_wheel.value)
        } catch(error){
            console.error(error)
        }
    }

    const emit = defineEmits(['creation-info'])

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            image.value = file;
        }
    }

    const emitirCreacion = async()=>{
        let payload = {}

        switch (props.eleccion) {
            case 'fusion':
            case 'clear':
            case 'track':
            case 'tip':
            case 'tipe':
                payload = {
                    tipo: props.eleccion,
                    nombre: nombre.value,
                    descripcion: descripcion.value
                }
                break
            
            case 'bey':
                // Use FormData for file upload
                const formData = new FormData();
                formData.append('tipo', 'bey');
                formData.append('nombre', nombre.value);
                formData.append('descripcion', descripcion.value);
                formData.append('fusion', fusion_wheel.value);
                formData.append('clear', clear_wheel.value);
                formData.append('track', track.value);
                formData.append('tip', tip.value);
                formData.append('tipe', tipe.value);
                formData.append('color', color.value)
                if (image.value) {
                    formData.append('image', image.value);
                }
                
                payload = formData;
                break
        }
        emit('creation-info', payload)
    }

    cargarOpciones()
</script>
<template>
    <form action="post">
        <div class="relative flex flex-col justify-center items-center p-6 m-6 border-2 border-black rounded-lg gap-4 bg-white w-fit">
            <div  v-if="eleccion === 'fusion'">
                <h3 class="text-sm">Nombre</h3>
                <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
            </div>
            <div class="camposClear" v-if="eleccion === 'clear'">
                <h3 class="text-sm">Nombre</h3>
                <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
            </div>
            <div class="camposTrack" v-if="eleccion === 'track'">
                <h3 class="text-sm">Nombre</h3>
                <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
            </div>
            <div class="camposTip" v-if="eleccion === 'tip'">
                <h3 class="text-sm">Nombre</h3>
                <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
            </div>
            <div class="camposTipe" v-if="eleccion === 'tipe'">
                <h3 class="text-sm">Nombre</h3>
                <input class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
            </div>
            <div class="camposBey" v-if="eleccion === 'bey'">
                <h3 class="text-sm">Nombre</h3>
                <input placeholder="Agrega el nombre del beyblade" class="bg-gray-200 w-[300px]" type="text" v-model="nombre">
                <h3 class="text-sm">Descripción</h3>
                <textarea placeholder="Agrega una descripción del beyblade" class="bg-gray-200" v-model="descripcion" rows="4" cols="100"></textarea>
                <h3 class="text-sm">Fusion Wheel</h3>
                <select class="bg-gray-200 w-[300px]" v-model="fusion_wheel">
                    <option disabled value="">Seleccionar Rueda de fusion</option>
                    <option 
                        v-for="f in fusionWheels"
                        :key="f.id"
                        :value="f.id">
                    {{ f.nombre }}
                    </option>
                </select>
                <h3 class="text-sm">Clear Wheel</h3>
                <select class="bg-gray-200 w-[300px]" v-model="clear_wheel">
                    <option disabled>Seleccionar Aro de energía</option>
                    <option
                        v-for="c in clearWheels" 
                        :key="c.id"
                        :value="c.id">
                        {{ c.nombre }}
                    </option>
                </select>
                <h3 class="text-sm">Spin Track</h3>
                <select  class="bg-gray-200 w-[300px]" v-model="track">
                    <option disabled value="">Seleccionar Eje de rotación</option>
                    <option
                        v-for="t in tracks" 
                        :key="t.id"
                        :value="t.id">
                        {{ t.nombre }}
                    </option>
                </select>
                <h3 class="text-sm">Tip</h3>
                <select class="bg-gray-200 w-[300px]" v-model="tip">
                    <option disabled value="">Seleccionar Punta de rendimiento</option>
                    <option
                        v-for="t in tips"
                        :key="t.id" 
                        :value="t.id">
                        {{ t.nombre }}
                    </option>
                </select>                                                      
                <h3 class="text-sm">Tipe</h3>
                <select class="bg-gray-200 w-[300px]" v-model="tipe">
                    <option disabled value="">Seleccionar Tipo</option>
                    <option 
                        v-for="t in tipes"
                        :key="t.id"
                        :value="t.id">
                        {{ t.nombre }}
                    </option>
                </select>
                <h3 class="text-sm">Color Predominante</h3>
                <input class="bg-gray-200 w-[300px]" v-model="color" type="text" placeholder="Ingresa color en ingles o codigo de color" >
                <h3 class="text-sm">Imagen</h3>
                <div class="flex justify-center border-2 border-black bg-gray-200 max-w-md p-6 h-auto mb-4 mr-6 rounded-lg">
                    <input type="file" @change="handleImageChange" accept="image/*">
                </div>
            </div>
            <router-link to="/home">
                <BaseButton :color="'Cyan'" @click="emitirCreacion()">Crear</BaseButton>
            </router-link>
        </div>
    </form>

</template>
<style>
    .campos{
        display: flex;
        flex-direction: column;
        margin: 10px;
    }
    .campos.camposFusion{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 10px;
        max-width: 500px;
        align-items: stretch;
        
    }

    .campos.camposFusion input{
        height: 30px;
    }

    .campos h3{
        margin: 0;
        color: azure;
    }

    .form{
        display: flex;
        justify-content: center;
        align-items: flex-start;

    }

    .form form{
        width: 100%;
        max-width: 500px;
    }

    .crear{
        display: block;
        margin: 20px auto;
    }
</style>