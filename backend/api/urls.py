from django.urls import path
from .views import *

urlpatterns = [
    path('crear/beyblade', crear_beyblade, name = "crear_beyblade"),
    path('crear/pieza', crear_pieza, name = "crear_pieza"),
    path('cargar/pieza', cargar_pieza, name = "cargar_pieza"),
    path('cargar/fusion', cargar_fusion, name = "cargar_fusion"),
    path('cargar/clear', cargar_clear, name = "cargar_clear"),
    path('cargar/track', cargar_track, name = "cargar_track"),
    path('cargar/tip', cargar_tip, name = "cargar_tip"),
    path('cargar/tipe', cargar_tipe, name = "cargar_tipe"),
    path('cargar/beyblade', cargar_beyblades, name = "cargar_beyblade"),
    path('cargar/bey/<int:pk>', cargar_bey, name = "cargar_bey"),
    path('editar/bey/<int:pk>', editar_beyblade, name = "editar_bey"),
    path('eliminar/bey/<int:pk>', eliminar_bey, name = "eliminar_bey"),

    path('crear/chat', crear_chat, name = "crear_chat"),
    path('cargar/chat/<int:pk>', cargar_chat, name = "cargar_chat"),
    path('cargar/chats', cargar_chats, name = "cargar_chats"),
    path('cargar/usuarios', cargar_usuarios, name = "cargar_usuarios"),
    path('crear/mensaje', crear_mensaje, name = "crear_mensaje"),
    path('eliminar/chat/<int:pk>', eliminar_chat, name = "eliminar_chat"),
    path('buscador', buscador, name = "buscador"),
    # Personajes endpoints
    path('crear/personaje', agregar_personaje, name="agregar_personaje"),
    path('editar/personaje/<int:pk>', editar_personaje, name="editar_personaje"),
    path('eliminar/personaje/<int:pk>', eliminar_personaje, name="eliminar_personaje"),
    path('cargar/personajes', cargar_personajes, name="cargar_personajes"),
    path('cargar/personaje/<int:pk>', cargar_personajes, name="cargar_personaje"),
    # Perfil de usuario endpoints
    path('perfil/usuario', cargar_perfil_usuario, name="cargar_perfil_usuario"),
    path('perfil/usuario/<int:pk>', cargar_perfil_usuario, name="cargar_perfil_usuario_pk"),
    path('editar/perfil', editar_perfil_usuario, name="editar_perfil_usuario"),
    path('verificar/password', verificar_password, name="verificar_password"),
    path('cambiar/password', cambiar_password, name="cambiar_password"),
    # Reportes y Sugerencias endpoints
    path('crear/reporte', crear_reporte, name="crear_reporte"),
    path('cargar/reportes', cargar_reportes, name="cargar_reportes"),
    path('responder/reporte/<int:pk>', responder_reporte, name="responder_reporte"),
    path('admin/cambiar/password', admin_cambiar_password, name="admin_cambiar_password"),
    path('admin/dar/admin', dar_permisos_admin, name="admin-dar-admin"),
]




