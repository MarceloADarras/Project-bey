from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F
from django.db import IntegrityError
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.models import chatUsuario

@api_view(["GET"])
def cargar_usuarios(request):
    usuarios = User.objects.all().order_by('id')

    data = []
    for i in usuarios:
        data.append({
            "id": i.id,
            "nombre": f"{i.first_name} {i.last_name}".strip() or i.username,
            "first_name": i.first_name,
            "last_name": i.last_name,
            "correo": i.email,
            "username": i.username,
            "is_staff": i.is_staff or i.is_superuser,
            "is_superuser": i.is_superuser,
            "date_joined": i.date_joined.strftime("%d/%m/%Y") if i.date_joined else None
        })
    
    return Response(data)



@api_view(["GET"])
def cargar_perfil_usuario(request, pk=None):
    try:
        user_obj = None
        if pk:
            try:
                user_obj = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        elif request.user and request.user.is_authenticated:
            user_obj = request.user
        else:
            user_id = request.query_params.get("user_id")
            if user_id:
                try:
                    user_obj = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not user_obj:
            return Response({"error": "No se pudo identificar el usuario activo"}, status=status.HTTP_401_UNAUTHORIZED)

        chats_count = chatUsuario.objects.filter(id_usuario=user_obj).count()
        
        data = {
            "id": user_obj.id,
            "username": user_obj.username,
            "email": user_obj.email,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "full_name": f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username,
            "date_joined": user_obj.date_joined.strftime("%d/%m/%Y") if user_obj.date_joined else None,
            "last_login": user_obj.last_login.strftime("%d/%m/%Y %H:%M") if user_obj.last_login else None,
            "chats_count": chats_count,
            "is_staff": user_obj.is_staff or user_obj.is_superuser,
            "is_superuser": user_obj.is_superuser
        }
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al cargar perfil: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def editar_perfil_usuario(request):
    try:
        user_id = request.data.get("user_id")
        user_obj = None
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not user_obj:
            return Response({"error": "No se pudo identificar el usuario"}, status=status.HTTP_401_UNAUTHORIZED)

        first_name = request.data.get("first_name", "").strip()
        last_name = request.data.get("last_name", "").strip()
        username = request.data.get("username", "").strip()
        email = request.data.get("email", "").strip()

        if not username:
            return Response({"error": "El nombre de usuario no puede estar vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # Check unique username
        if User.objects.filter(username=username).exclude(pk=user_obj.id).exists():
            return Response({"error": f"El nombre de usuario '{username}' ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)

        # Check unique email
        if email and User.objects.filter(email=email).exclude(pk=user_obj.id).exists():
            return Response({"error": f"El correo '{email}' ya está registrado con otra cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.username = username
        user_obj.email = email
        user_obj.save()

        return Response({
            "message": "Perfil actualizado con éxito",
            "user": {
                "id": user_obj.id,
                "username": user_obj.username,
                "email": user_obj.email,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "full_name": f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Error al actualizar perfil: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def verificar_password(request):
    try:
        user_id = request.data.get("user_id")
        password_actual = request.data.get("password_actual", "")

        user_obj = None
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not user_obj:
            return Response({"error": "No se pudo identificar el usuario"}, status=status.HTTP_401_UNAUTHORIZED)

        if not password_actual:
            return Response({"valid": False, "error": "Debes ingresar tu contraseña actual"}, status=status.HTTP_400_BAD_REQUEST)

        if user_obj.check_password(password_actual):
            return Response({"valid": True, "message": "Contraseña correcta"}, status=status.HTTP_200_OK)
        else:
            return Response({"valid": False, "error": "La contraseña actual es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Error al verificar contraseña: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def cambiar_password(request):
    try:
        user_id = request.data.get("user_id")
        password_actual = request.data.get("password_actual", "")
        password_nueva = request.data.get("password_nueva", "")
        password_confirmacion = request.data.get("password_confirmacion", "")

        user_obj = None
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not user_obj:
            return Response({"error": "No se pudo identificar el usuario"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify current password
        if not user_obj.check_password(password_actual):
            return Response({"error": "La contraseña actual es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        if not password_nueva:
            return Response({"error": "Debes ingresar una nueva contraseña"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password_nueva) < 6:
            return Response({"error": "La nueva contraseña debe tener al menos 6 caracteres"}, status=status.HTTP_400_BAD_REQUEST)

        if password_nueva != password_confirmacion:
            return Response({"error": "Las contraseñas nuevas no coinciden"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj.set_password(password_nueva)
        user_obj.save()

        return Response({"message": "Contraseña cambiada con éxito"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Error al cambiar contraseña: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def admin_cambiar_password(request):
    try:
        requester_id = request.data.get("admin_id")
        requester = None
        if request.user and request.user.is_authenticated:
            requester = request.user
        elif requester_id:
            try:
                requester = User.objects.get(pk=requester_id)
            except User.DoesNotExist:
                pass

        if not requester or not (requester.is_staff or requester.is_superuser):
            return Response({"error": "No tienes permisos de administrador para realizar esta acción"}, status=status.HTTP_403_FORBIDDEN)

        target_user_id = request.data.get("target_user_id")
        nueva_password = request.data.get("nueva_password", "").strip()

        if not target_user_id:
            return Response({"error": "Debe especificar el usuario a modificar"}, status=status.HTTP_400_BAD_REQUEST)

        if not nueva_password or len(nueva_password) < 6:
            return Response({"error": "La nueva contraseña debe tener al menos 6 caracteres"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(pk=target_user_id)
        except User.DoesNotExist:
            return Response({"error": "El usuario objetivo no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)

        target_user.set_password(nueva_password)
        target_user.save()

        return Response({
            "message": f"La contraseña del usuario '{target_user.username}' ha sido restablecida con éxito."
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al cambiar contraseña de emergencia: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def dar_permisos_admin(request):
    try:
        requester_id = request.data.get("admin_id")
        requester = None
        if request.user and request.user.is_authenticated:
             requester = request.user
        elif requester_id:
            try:
                requester = User.objects.get(pk=requester_id)
            except User.DoesNotExist:
                pass
        
        if not requester or not (requester.is_staff or requester.is_superuser):
                    return Response({"error": "No tienes permisos de administrador para realizar esta acción"}, status=status.HTTP_403_FORBIDDEN)

        target_user_id = request.data.get("target_user_id")

        if not target_user_id:
            return Response({"error": "Debe especificar el usuario a modificar"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(pk=target_user_id)
        except User.DoesNotExist:
            return Response({"error": "El usuario objetivo no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)

        target_user.is_staff = True
        target_user.save()

        return Response({
                "message": "Se han otorgado permisos de administrador correctamente"
        }, status=status.HTTP_200_OK)



    except Exception as e:
        return Response({"error": f"Error al dar permisos de administrador: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


