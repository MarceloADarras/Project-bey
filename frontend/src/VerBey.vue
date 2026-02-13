<script setup>
    import Header from '../components/HeaderComponent.vue'
    import router from '../router';
    import { useRoute, useRouter } from 'vue-router';
    import api from './main';
    import { ref, resolveDirective, watch } from 'vue';
    import BeyComponent from '../components/BeyComponent.vue';
    import BaseButton from '../components/BaseButton.vue';
    import ModalEliminarComponent from '../components/ModalEliminarComponent.vue';
    import ModalDetalleComponent from '../components/ModalDetalleComponent.vue';


    const route = useRoute();
    const ruta = useRouter();
    const id = route.params.id

    const mostrarModal = ref(false)

    const mostrarModalF = ref(false)
    const mostrarModalC = ref(false)
    const mostrarModalT = ref(false)
    const mostrarModalTi = ref(false)
    const mostrarModalTipe = ref(false)

    const bey = ref({});

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


    const abrirModalF = () => {
        mostrarModalF.value = true
    }

    const cerrarModalF = () => {
        mostrarModalF.value = false
    }

    const abrirModalC = () => {
        mostrarModalC.value = true
    }

    const cerrarModalC = () => {
        mostrarModalC.value = false
    }

    const abrirModalT = () => {
        mostrarModalT.value = true
    }

    const cerrarModalT = () => {
        mostrarModalT.value = false
    }

    const abrirModalTi = () => {
        mostrarModalTi.value = true
    }

    const cerrarModalTi = () => {
        mostrarModalTi.value = false
    }

    const abrirModalTipe = () => {
        mostrarModalTipe.value = true
    }

    const cerrarModalTipe = () => {
        mostrarModalTipe.value = false
    }
    

    cargarBeyblade()

</script>
<template>
    <Header></Header>
    
    <div class="flex items-center justify-center p-6">
        <div class="flex items-center justify-center gap-4">
            <div class="flex flex-col items-center justify-center gap-4">
                <img :src="bey.photo ? `http://127.0.0.1:8000${bey.photo}` : '../img/image.png'" class="h-auto w-[300px]">
                <BeyComponent
                    :nombre="bey.nombre"
                    :descripcion="bey.descripcion"
                ></BeyComponent>
            </div>

            <div class="contenedor-detalles">

                <div class="detalle" type="button" @click="abrirModalF">
                    <h2>Fusion Wheel</h2>
                </div>

                <div class="detalle" type="button" @click="abrirModalC">
                    <h2>Clear Wheel</h2>
                </div>

                <div class="detalle" type="button" @click="abrirModalT">
                    <h2>Spin Track</h2>
                </div>

                <div class="detalle" type="button" @click="abrirModalTi">
                    <h2>Performance Tip</h2>
                </div>

                <div class="detalle" type="button" @click="abrirModalTipe">
                    <h2>Tipe</h2>
                </div>
            </div>
        </div>
    </div>

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

    <div class="flex justify-center mt-4 p-4">
        <BaseButton :color="'#A61C1C'" :hover-color="'#E63946'" @click="abrirModal()">Eliminar</BaseButton>
    </div>

    <ModalEliminarComponent
        v-if="mostrarModal"
        :texto="'¿Seguro de que quieres eliminar el Beyblade?'"
        :textoBoton="'Eliminar'"
        :textoBoton2="'Cancelar'"
        :color="'Red'"
        :hover-color="'Cyan'"
        @eliminar="eliminarBey()"
        @cancelar="cerrarModal()"
    ></ModalEliminarComponent>
</template>
<style>
.main-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: calc(100vh - 70px);
    padding: 20px;
}

.content-wrapper {
    display: flex;
    gap: 40px;
    align-items: flex-start;
    max-width: 1200px;
    width: 100%;
}

.contenedor-detalles{
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 20px;
    flex: 0 0 auto;
}

.detalle{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 150px;
    height: 150px;
    padding: 20px;
    border: 2px solid #FF6B35;
    border-radius: 50%;
    transition: all 0.3s ease;
    background: #ffff;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.detalle:hover{
    transform: scale(1.1);
    background: rgba(230, 57, 70, 0.7);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    border: 2px solid #000;
    border-color: #000;
}

.detalle:hover h2 {
    color: #000;
}

.detalle h2 {
    margin: 0;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    color: #E63946;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.eliminar-container {
    display: flex;
    justify-content: center;
    margin-top: 40px;
}

/* Responsive design */
@media (max-width: 768px) {
    .content-wrapper {
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }
    
    .contenedor-detalles {
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        width: 100%;
    }
    
    .detalle {
        flex: 0 0 auto;
    }
    
    .eliminar-container {
        margin-top: 30px;
    }
}
</style>