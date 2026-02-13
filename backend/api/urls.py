from django.urls import path
from .views import *

urlpatterns = [
    path('crear/beyblade', crear_beyblade, name = "crear_beyblade"),
    path('crear/fusion', crear_fusion, name = "crear_fusion"),
    path('crear/clear', crear_clear, name = "crear_clear"),
    path('crear/track', crear_track, name = "crear_track"),
    path('crear/tip', crear_tip, name = "crear_tip"),
    path('crear/tipe', crear_tipe, name = "crear_tipe"),
    path('cargar/fusion', cargar_fusion, name = "cargar_fusion"),
    path('cargar/clear', cargar_clear, name = "cargar_clear"),
    path('cargar/track', cargar_track, name = "cargar_track"),
    path('cargar/tip', cargar_tip, name = "cargar_tip"),
    path('cargar/tipe', cargar_tipe, name = "cargar_tipe"),
    path('cargar/beyblade', cargar_beyblades, name = "cargar_beyblade"),
    path('cargar/bey/<int:pk>', cargar_bey, name = "cargar_bey"),
    path('eliminar/bey/<int:pk>', eliminar_bey, name = "eliminar_bey"),
    path('crear/chat', crear_chat, name = "crear_chat"),
    path('cargar/chat/<int:pk>', cargar_chat, name = "cargar_chat"),
    path('cargar/chats', cargar_chats, name = "cargar_chats"),
    path('cargar/usuarios', cargar_usuarios, name = "cargar_usuarios"),
    path('crear/mensaje', crear_mensaje, name = "crear_mensaje"),
    path('eliminar/chat/<int:pk>', eliminar_chat, name = "eliminar_chat"),
    path('buscador', buscador, name = "buscador"),
    path('beybot/chat', beybots_chat, name = "beybot_chat")
]