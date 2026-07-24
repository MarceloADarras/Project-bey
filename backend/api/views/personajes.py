from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Personaje, Beyblade
import json
import os
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name = "gcpljpzi",
    api_key = os.environ.get("API_KEY"),
    api_secret = os.environ.get("API_SECRET"),
    secure = True
)


def _get_image_url(image_field):
    if not image_field:
        return None
    url_str = str(image_field)
    if url_str.startswith("http://") or url_str.startswith("https://"):
        return url_str
    try:
        return image_field.url
    except Exception:
        return url_str


def _get_beyblade_ids(request, data=None):
    """Auxiliary helper to extract a list of Beyblade IDs from request data."""
    ids = []
    if data and isinstance(data, dict):
        raw = data.get("beyblades") if "beyblades" in data else data.get("beyblade")
        if isinstance(raw, list):
            ids = raw
        elif raw is not None and raw != "":
            ids = [raw]
    else:
        # Multipart / Form-Data
        raw_list = request.POST.getlist("beyblades") or request.POST.getlist("beyblade")
        if raw_list:
            ids = raw_list
        else:
            single = request.POST.get("beyblades") or request.POST.get("beyblade")
            if single:
                if isinstance(single, str) and "," in single:
                    ids = [x.strip() for x in single.split(",") if x.strip()]
                else:
                    ids = [single]
    
    # Filter out empty values and convert to int/string
    clean_ids = []
    for val in ids:
        if val is not None and str(val).strip() != "":
            clean_ids.append(val)
    return clean_ids


@api_view(["POST"])
def agregar_personaje(request):
    try:
        data = None
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            nombre = data.get("nombre")
            altura = data.get("altura", "")
            peso = data.get("peso", "")
            personalidad = data.get("personalidad", "")
            historia = data.get("historia", "")
            foto = None
        else:
            nombre = request.POST.get("nombre")
            altura = request.POST.get("altura", "")
            peso = request.POST.get("peso", "")
            personalidad = request.POST.get("personalidad", "")
            historia = request.POST.get("historia", "")
            foto_file = request.FILES.get("foto") if 'foto' in request.FILES else None
            if foto_file:
                try:
                    upload_result = cloudinary.uploader.upload(foto_file, folder="personajes")
                    foto = upload_result.get("secure_url") or upload_result.get("url")
                except Exception as cloud_err:
                    print(f"Error subiendo a Cloudinary: {cloud_err}")
                    foto = foto_file
            else:
                foto = None

        if not nombre:
            return Response({"error": "El nombre es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        beyblade_ids = _get_beyblade_ids(request, data)

        personaje = Personaje.objects.create(
            nombre=nombre,
            altura=altura,
            peso=peso,
            personalidad=personalidad,
            historia=historia,
            foto=foto
        )

        if beyblade_ids:
            bey_objs = Beyblade.objects.filter(id__in=beyblade_ids)
            personaje.beyblades.set(bey_objs)

        return Response({
            "success": "Personaje creado con éxito",
            "id": personaje.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Error al agregar personaje: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT", "POST"])
def editar_personaje(request, pk):
    try:
        try:
            personaje = Personaje.objects.get(pk=pk)
        except Personaje.DoesNotExist:
            return Response({"error": "El personaje no existe"}, status=status.HTTP_404_NOT_FOUND)

        data = None
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            personaje.nombre = data.get("nombre", personaje.nombre)
            personaje.altura = data.get("altura", personaje.altura)
            personaje.peso = data.get("peso", personaje.peso)
            personaje.personalidad = data.get("personalidad", personaje.personalidad)
            personaje.historia = data.get("historia", personaje.historia)
        else:
            personaje.nombre = request.POST.get("nombre", personaje.nombre)
            personaje.altura = request.POST.get("altura", personaje.altura)
            personaje.peso = request.POST.get("peso", personaje.peso)
            personaje.personalidad = request.POST.get("personalidad", personaje.personalidad)
            personaje.historia = request.POST.get("historia", personaje.historia)
            if 'foto' in request.FILES:
                foto_file = request.FILES.get("foto")
                if foto_file:
                    try:
                        upload_result = cloudinary.uploader.upload(foto_file, folder="personajes")
                        personaje.foto = upload_result.get("secure_url") or upload_result.get("url")
                    except Exception as cloud_err:
                        print(f"Error subiendo a Cloudinary: {cloud_err}")
                        personaje.foto = foto_file

        # Check if beyblades field was sent in payload
        has_beyblades_key = False
        if data and isinstance(data, dict):
            has_beyblades_key = ("beyblades" in data) or ("beyblade" in data)
        else:
            has_beyblades_key = ("beyblades" in request.POST) or ("beyblade" in request.POST)

        if has_beyblades_key:
            beyblade_ids = _get_beyblade_ids(request, data)
            bey_objs = Beyblade.objects.filter(id__in=beyblade_ids) if beyblade_ids else []
            personaje.beyblades.set(bey_objs)

        personaje.save()
        return Response({"success": "Personaje actualizado con éxito"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al editar personaje: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE", "POST"])
def eliminar_personaje(request, pk):
    try:
        personaje = Personaje.objects.get(pk=pk)
        personaje.delete()
        return Response({"success": "Personaje eliminado con éxito"}, status=status.HTTP_200_OK)
    except Personaje.DoesNotExist:
        return Response({"error": "El personaje no existe"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error al eliminar personaje: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def cargar_personajes(request, pk=None):
    try:
        if pk is not None:
            try:
                p = Personaje.objects.get(pk=pk)
            except Personaje.DoesNotExist:
                return Response({"error": "Personaje no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            beyblades_data = []
            for bey in p.beyblades.all():
                beyblades_data.append({
                    "id": bey.id,
                    "nombre": bey.nombre,
                    "descripcion": bey.descripcion,
                    "photo": _get_image_url(bey.photo),
                    "fusion": bey.fusion_wheel.nombre if bey.fusion_wheel else "",
                    "descripcion1": bey.fusion_wheel.descripcion if bey.fusion_wheel else "",
                    "clear": bey.clear_wheel.nombre if bey.clear_wheel else "",
                    "descripcion2": bey.clear_wheel.descripcion if bey.clear_wheel else "",
                    "track": bey.spin_track.nombre if bey.spin_track else "",
                    "descripcion3": bey.spin_track.descripcion if bey.spin_track else "",
                    "tip": bey.tip.nombre if bey.tip else "",
                    "descripcion4": bey.tip.descripcion if bey.tip else "",
                    "tipe": bey.tipe.nombre if bey.tipe else "",
                    "descripcion5": bey.tipe.descripcion if bey.tipe else "",
                    "color": bey.color,
                    "season": bey.season
                })

            data = {
                "id": p.id,
                "nombre": p.nombre,
                "altura": p.altura,
                "peso": p.peso,
                "personalidad": p.personalidad,
                "historia": p.historia,
                "foto": _get_image_url(p.foto),
                "beyblades": beyblades_data,
                # Backwards compatible single beyblade field
                "beyblade": beyblades_data[0] if len(beyblades_data) > 0 else None
            }
            return Response(data, status=status.HTTP_200_OK)

        personajes = Personaje.objects.all()
        data = []
        for p in personajes:
            beys = p.beyblades.all()
            beys_list = [
                {
                    "id": b.id,
                    "nombre": b.nombre,
                    "photo": _get_image_url(b.photo),
                    "season": b.season
                }
                for b in beys
            ]
            names_str = ", ".join([b.nombre for b in beys]) if beys else None

            data.append({
                "id": p.id,
                "nombre": p.nombre,
                "altura": p.altura,
                "peso": p.peso,
                "personalidad": p.personalidad,
                "historia": p.historia,
                "foto": _get_image_url(p.foto),
                "beyblades": beys_list,
            })
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al cargar personajes: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

