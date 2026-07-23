from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from api.models import Reporte
import json

def purge_old_rejected_reports():
    """Automatically deletes rejected reports older than 30 days."""
    try:
        limite = timezone.now() - timedelta(days=30)
        reportes_viejos = Reporte.objects.filter(estado='rechazado', created_at__lt=limite)
        count = reportes_viejos.count()
        if count > 0:
            reportes_viejos.delete()
            print(f"Se eliminaron automáticamente {count} reportes rechazados de más de 30 días.")
    except Exception as e:
        print(f"Error al purgar reportes viejos: {e}")


@api_view(["POST"])
def crear_reporte(request):
    try:
        data = None
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            tipo = data.get("tipo", "beyblade")
            nombre = data.get("nombre", "").strip()
            descripcion = data.get("descripcion", "").strip()
            opcional = data.get("opcional", "").strip()
            user_id = data.get("user_id")
        else:
            tipo = request.POST.get("tipo", "beyblade")
            nombre = request.POST.get("nombre", "").strip()
            descripcion = request.POST.get("descripcion", "").strip()
            opcional = request.POST.get("opcional", "").strip()
            user_id = request.POST.get("user_id")

        if not nombre:
            return Response({"error": "El nombre del elemento a sugerir es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = None
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not user_obj:
            return Response({"error": "No se pudo identificar el usuario que realiza la sugerencia"}, status=status.HTTP_401_UNAUTHORIZED)

        reporte = Reporte.objects.create(
            usuario=user_obj,
            tipo=tipo,
            nombre=nombre,
            descripcion=descripcion,
            opcional=opcional,
            estado='pendiente'
        )

        return Response({
            "success": "Sugerencia enviada correctamente. El equipo de administración la revisará pronto.",
            "id": reporte.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Error al crear sugerencia: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def cargar_reportes(request):
    try:
        # Purge rejected reports older than 30 days
        purge_old_rejected_reports()

        user_obj = None
        user_id = request.query_params.get("user_id")
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                pass

        if not user_obj:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        if user_obj.is_staff or user_obj.is_superuser:
            reportes = Reporte.objects.all().order_by('-created_at')
        else:
            reportes = Reporte.objects.filter(usuario=user_obj).order_by('-created_at')

        data = []
        for r in reportes:
            data.append({
                "id": r.id,
                "usuario_id": r.usuario.id,
                "usuario_nombre": f"{r.usuario.first_name} {r.usuario.last_name}".strip() or r.usuario.username,
                "username": r.usuario.username,
                "tipo": r.tipo,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "opcional": r.opcional,
                "estado": r.estado,
                "estado_display": r.get_estado_display(),
                "created_at": r.created_at.strftime("%d/%m/%Y %H:%M"),
                "fecha_respuesta": r.fecha_respuesta.strftime("%d/%m/%Y %H:%M") if r.fecha_respuesta else None
            })

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al cargar sugerencias: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def responder_reporte(request, pk):
    try:
        user_id = request.data.get("user_id")
        user_obj = None
        if request.user and request.user.is_authenticated:
            user_obj = request.user
        elif user_id:
            try:
                user_obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                pass

        if not user_obj or not (user_obj.is_staff or user_obj.is_superuser):
            return Response({"error": "No tienes permisos de administrador para responder sugerencias"}, status=status.HTTP_403_FORBIDDEN)

        try:
            reporte = Reporte.objects.get(pk=pk)
        except Reporte.DoesNotExist:
            return Response({"error": "La sugerencia no existe"}, status=status.HTTP_404_NOT_FOUND)

        nuevo_estado = request.data.get("estado")
        if nuevo_estado not in ['aceptado', 'rechazado']:
            return Response({"error": "Estado inválido. Debe ser 'aceptado' o 'rechazado'"}, status=status.HTTP_400_BAD_REQUEST)

        reporte.estado = nuevo_estado
        reporte.fecha_respuesta = timezone.now()
        reporte.save()

        return Response({
            "success": f"La sugerencia ha sido marcada como '{reporte.get_estado_display()}'"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al responder la sugerencia: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
