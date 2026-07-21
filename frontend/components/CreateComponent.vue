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
    const sistema = ref("")
    const season = ref("")

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
                const all = await api.get("cargar/pieza")
                const fus = await api.get("cargar/fusion")
                const cle = await api.get("cargar/clear")
                const tra = await api.get("cargar/track")
                const pun = await api.get("cargar/tip")
                const tipo = await api.get("cargar/tipe")

                console.log(all.data)

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
                formData.append('season', season.value);
                formData.append('sistem', sistema.value);
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
    <form @submit.prevent="emitirCreacion" class="w-full max-w-2xl">
        <div class="glass-card relative flex flex-col justify-center items-center p-8 rounded-2xl gap-5 w-full shadow-xl text-slate-900">
            <div v-if="eleccion === 'fusion'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="4"></textarea>
                </div>
            </div>

            <div v-if="eleccion === 'clear'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="4"></textarea>
                </div>
            </div>

            <div v-if="eleccion === 'track'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="4"></textarea>
                </div>
            </div>

            <div v-if="eleccion === 'tip'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="4"></textarea>
                </div>
            </div>

            <div v-if="eleccion === 'tipe'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="4"></textarea>
                </div>
            </div>

            <div v-if="eleccion === 'bey'" class="w-full space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre</label>
                    <input placeholder="Agrega el nombre del beyblade" class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" type="text" v-model="nombre" required>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Descripción</label>
                    <textarea placeholder="Agrega una descripción del beyblade" class="w-full bg-white/90 border border-slate-300 text-slate-900 p-3 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="descripcion" rows="3"></textarea>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Fusion Wheel</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="fusion_wheel">
                            <option disabled value="">Seleccionar Rueda de fusión</option>
                            <option v-for="f in fusionWheels" :key="f.id" :value="f.id">{{ f.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Clear Wheel</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="clear_wheel">
                            <option disabled value="">Seleccionar Aro de energía</option>
                            <option v-for="c in clearWheels" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Spin Track</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="track">
                            <option disabled value="">Seleccionar Eje de rotación</option>
                            <option v-for="t in tracks" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Tip</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="tip">
                            <option disabled value="">Seleccionar Punta de rendimiento</option>
                            <option v-for="t in tips" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Tipe</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="tipe">
                            <option disabled value="">Seleccionar Tipo</option>
                            <option v-for="t in tipes" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Temporada</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="season">
                            <option disabled value="">Seleccionar la temporada</option>
                            <option value="Metal Fusion">Metal Fusion</option>
                            <option value="Metal Masters">Metal Masters</option>
                            <option value="Metal Fury">Metal Fury</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Sistema</label>
                        <select class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="sistema">
                            <option disabled value="">Seleccionar el sistema</option>
                            <option value="Pre-Hybrid">Sistema Pre-Híbrido</option>
                            <option value="Hybrid">Sistema Híbrido</option>
                            <option value="4D">Sistema 4D</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Color Predominante</label>
                        <input class="w-full bg-white/90 border border-slate-300 text-slate-900 px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500 shadow-inner" v-model="color" type="text" placeholder="Código hex o nombre en inglés">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Imagen</label>
                    <div class="border border-slate-300 bg-white/90 p-4 rounded-xl shadow-inner">
                        <input type="file" @change="handleImageChange" accept="image/*" class="text-xs text-slate-700 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-amber-500 file:text-white hover:file:bg-amber-600">
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <BaseButton color="#FF6B35" hoverColor="#E63946" @click="emitirCreacion()">Crear</BaseButton>
            </div>
        </div>
    </form>
</template>


<style scoped>
</style>