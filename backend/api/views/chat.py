from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F
from django.db import IntegrityError
from rest_framework.views import APIView
from api.models import Chat, chatUsuario, Mensaje
from django.contrib.auth.models import User
from api.serializers import ChatDetalleSerializer, MensajeCreateSerializer, MensajeSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def crear_chat(request):
    user = request.user
    
    if not user:
        return Response(
            {"error": "Usuario creador no existe"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user_select = request.data.get("id_usuario")

    try:
        user2 = User.objects.get(id=user_select)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuario seleccionado no existe"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    nombre_chat = request.data.get("nombre")

    try:
        chat = Chat.objects.get(nombre=nombre_chat)
        if chat:
            return Response(
                {"error": "El chat ya existe"},
                status=status.HTTP_303_SEE_OTHER
            )
    except Chat.DoesNotExist:
        pass


    if nombre_chat:
        Chat.objects.create(nombre = nombre_chat)
        chat = Chat.objects.get(nombre=nombre_chat)
    else:
        return Response(
            {"error": "No se recibió nombre de chat"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    chatUsuario.objects.create(id_usuario = user, id_chat = chat)
    chatUsuario.objects.create(id_usuario = user2, id_chat = chat)

    return Response(
        {"success": "Chat creado con exito"},
        status=status.HTTP_201_CREATED
    )

@api_view(["GET"])
def cargar_chat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
    except Chat.DoesNotExist:
        return Response(
            {"error": "El chat seleccionado no existe"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ChatDetalleSerializer(chat)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def cargar_chats(request):
    user = request.user

    try:
        chats = chatUsuario.objects.filter(id_usuario=user)
        print(chats)
    except Exception as e:
        return Response(
            {"error": "No existen chats asociados al usuario"},
            status=status.HTTP_404_NOT_FOUND
        )

    data = []

    for c in chats:
        list = {
            "id": c.id_chat.id,
            "nombre": c.id_chat.nombre
        }
        data.append(list)
    
    return Response(data)

@api_view(["POST"])
def crear_mensaje(request):
    usuario = request.user

    if usuario is None or not usuario.is_authenticated:
        return Response(
            {"error": "Usuario no iniciado"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = MensajeCreateSerializer(
        data=request.data,
        context={"user": usuario},
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data

    mensaje = Mensaje.objects.create(
        id_usuario=usuario,
        id_chat=data["chat_obj"],
        texto=data.get("texto"),
        archivo=data.get("archivo"),
        url=data.get("enlace"),
    )

    return Response(MensajeSerializer(mensaje).data, status = status.HTTP_201_CREATED)

@api_view(["DELETE"])
def eliminar_chat(request, pk):
    try:
        chat = Chat.objects.get(pk = pk)
    except Chat.DoesNotExist:
        return Response(
            {"error": "El chat a eliminar no existe o no se encuentra"},
            status=status.HTTP_404_NOT_FOUND
        )
    
   
    chatUser = chatUsuario.objects.filter(id_chat=chat)
   
    
    for ch in chatUser:
        ch.delete()

    mensajes = Mensaje.objects.filter(id_chat=chat)

    for men in mensajes:
        men.delete()

    return Response(
        {"success": "Se ha eliminado el chat correctamente"},
        status=status.HTTP_200_OK
    )
    

    


    



