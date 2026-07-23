<script setup>
    import Header from '../components/HeaderComponent.vue'
    import router from '../router';
    import { useRoute, useRouter } from 'vue-router';
    import api from './main';
    import { ref, watch } from 'vue';
    import BeyComponent from '../components/BeyComponent.vue';
    import BaseButton from '../components/BaseButton.vue';
    import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
    import ModalDetalleComponent from '../components/ModalDetalleComponent.vue';
    import ModalEditarBeyComponent from '../components/ModalEditarBeyComponent.vue';

    const route = useRoute();
    const ruta = useRouter();
    const id = route.params.id;

    const mostrarModal = ref(false);
    const mostrarModalEditar = ref(false);

    const mostrarModalF = ref(false);
    const mostrarModalC = ref(false);
    const mostrarModalT = ref(false);
    const mostrarModalTi = ref(false);
    const mostrarModalTipe = ref(false);

    const bey = ref({});

    const getPhotoUrl = (photo) => {
        if (!photo) return '/img/image.png';
        if (photo.startsWith('http')) return photo;
        return `https://project-bey-production.up.railway.app${photo}`;
    };

    const cargarBeyblade = async() => {
        try{
            const res = await api.get(`cargar/bey/${id}`)
            bey.value = res.data
            console.log(bey.value)
        } catch(error){
            console.error(error)
        }
    }

    const eliminarBey = async() => {
        try{
            await api.delete(`eliminar/bey/${id}`)
            console.log("Eliminación completa")
            ruta.push('/home');
        } catch(error){
            console.error(error)
        }
    }

    const abrirModal = () => {
        mostrarModal.value = true
    }

    const cerrarModal = () => {
        mostrarModal.value = false
    }

    const abrirModalF = () => { mostrarModalF.value = true }
    const cerrarModalF = () => { mostrarModalF.value = false }
    const abrirModalC = () => { mostrarModalC.value = true }
    const cerrarModalC = () => { mostrarModalC.value = false }
    const abrirModalT = () => { mostrarModalT.value = true }
    const cerrarModalT = () => { mostrarModalT.value = false }
    const abrirModalTi = () => { mostrarModalTi.value = true }
    const cerrarModalTi = () => { mostrarModalTi.value = false }
    const abrirModalTipe = () => { mostrarModalTipe.value = true }
    const cerrarModalTipe = () => { mostrarModalTipe.value = false }

    cargarBeyblade()
</script>

<template>
    <Header></Header>
    
    <div class="flex flex-col items-center justify-center p-6 max-w-5xl mx-auto min-h-[calc(100vh-64px)]">
        <div class="glass-card flex flex-col md:flex-row items-center justify-center gap-8 p-8 rounded-2xl w-full">
            <div class="flex flex-col items-center justify-center gap-4">
                <img :src="getPhotoUrl(bey.photo)" class="h-auto w-64 object-contain rounded-xl shadow-lg border border-white/20 p-2 bg-black/20">
                <BeyComponent
                    :nombre="bey.nombre"
                    :descripcion="bey.descripcion"
                ></BeyComponent>
            </div>

            <div class="contenedor-detalles">
                <div class="detalle glass-card" type="button" @click="abrirModalF">
                    <h2>Fusion Wheel</h2>
                </div>

                <div class="detalle glass-card" type="button" @click="abrirModalC">
                    <h2>Clear Wheel</h2>
                </div>

                <div class="detalle glass-card" type="button" @click="abrirModalT">
                    <h2>Spin Track</h2>
                </div>

                <div class="detalle glass-card" type="button" @click="abrirModalTi">
                    <h2>Performance Tip</h2>
                </div>

                <div class="detalle glass-card" type="button" @click="abrirModalTipe">
                    <h2>Tipe</h2>
                </div>
            </div>
        </div>

        <div class="flex items-center justify-center gap-4 mt-6">
            <BaseButton :color="'#FF6B35'" :hover-color="'#E63946'" @click="mostrarModalEditar = true">✏️ Editar Beyblade</BaseButton>
            <BaseButton :color="'#E63946'" :hover-color="'#C1121F'" @click="abrirModal()">🗑️ Eliminar</BaseButton>
        </div>
    </div>

    <!-- Edit Beyblade Modal -->
    <ModalEditarBeyComponent
        v-if="mostrarModalEditar"
        :bey-id="id"
        @cerrar="mostrarModalEditar = false"
        @actualizado="cargarBeyblade"
    />

    <ModalDetalleComponent
        v-if="mostrarModalF"
        :titulo="bey.fusion"
        :detalle="bey.descripcion1"
        @cerrar="cerrarModalF()"
    ></ModalDetalleComponent>

    <ModalDetalleComponent
        v-if="mostrarModalC"
        :titulo="bey.clear"
        :detalle="bey.descripcion2"
        @cerrar="cerrarModalC()"
    ></ModalDetalleComponent>

    <ModalDetalleComponent
        v-if="mostrarModalT"
        :titulo="bey.track"
        :detalle="bey.descripcion3"
        @cerrar="cerrarModalT()"
    ></ModalDetalleComponent>

    <ModalDetalleComponent
        v-if="mostrarModalTi"
        :titulo="bey.tip"
        :detalle="bey.descripcion4"
        @cerrar="cerrarModalTi()"
    ></ModalDetalleComponent>

    <ModalDetalleComponent
        v-if="mostrarModalTipe"
        :titulo="bey.tipe"
        :detalle="bey.descripcion5"
        @cerrar="cerrarModalTipe()"
    ></ModalDetalleComponent>

    <ModalEliminarComponent
        v-if="mostrarModal"
        :texto="'¿Seguro de que quieres eliminar el Beyblade?'"
        :textoBoton="'Eliminar'"
        :textoBoton2="'Cancelar'"
        :color="'#E63946'"
        :hover-color="'#B71C1C'"
        @eliminar="eliminarBey()"
        @cancelar="cerrarModal()"
    ></ModalEliminarComponent>
</template>

<style scoped>
.contenedor-detalles {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 10px;
    flex: 0 0 auto;
}

.detalle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 140px;
    height: 140px;
    padding: 16px;
    border: 2px solid rgba(255, 107, 53, 0.7);
    border-radius: 50%;
    transition: all 0.25s ease;
    background: rgba(15, 23, 42, 0.9);
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    text-align: center;
}

.detalle:hover {
    transform: scale(1.08) translateY(-2px);
    background: linear-gradient(135deg, rgba(230, 57, 70, 0.9) 0%, rgba(255, 107, 53, 0.9) 100%);
    box-shadow: 0 8px 20px rgba(230, 57, 70, 0.4);
    border-color: #FFA500;
}

.detalle:hover h2 {
    color: #FFFFFF;
}

.detalle h2 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: #FF6B35;
    transition: color 0.2s ease;
}

@media (max-width: 768px) {
    .contenedor-detalles {
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        width: 100%;
    }
}
</style>