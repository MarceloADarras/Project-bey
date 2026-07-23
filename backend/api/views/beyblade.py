from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F
from django.db import IntegrityError
from rest_framework.views import APIView
from api.models import Beyblade, FusionWheel, ClearWheel, SpinTrack, Tip, Tipe
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



@api_view(["POST"])
def crear_beyblade(request):
    # Handle both JSON and form data (for file uploads)
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        fusion_wheel = data.get("fusion")
        clear_wheel = data.get("clear")
        spin_track = data.get("track")
        tip = data.get("tip")
        tipe = data.get("tipe")
        color = data.get("color")
        season = data.get("season")
        sistem = data.get("sistem")
        image = None
    else:
        # Handle form data (for file uploads)
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        fusion_wheel = request.POST.get("fusion")
        clear_wheel = request.POST.get("clear")
        spin_track = request.POST.get("track")
        tip = request.POST.get("tip")
        tipe = request.POST.get("tipe")
        color = request.POST.get("color")
        season = request.POST.get("season")
        sistem = request.POST.get("sistem")
        image_file = request.FILES.get("image") if 'image' in request.FILES else None
        if image_file:
            try:
                upload_result = cloudinary.uploader.upload(image_file, folder="beyblades")
                image = upload_result.get("secure_url") or upload_result.get("url")
            except Exception as cloud_err:
                print(f"Error subiendo beyblade a Cloudinary: {cloud_err}")
                image = image_file
        else:
            image = None

    # Validate required fields
    if not all([nombre, descripcion, fusion_wheel, clear_wheel, spin_track, tip, tipe, color, season, sistem]):
        return Response(
            {"error": "Faltan campos requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        fusion = FusionWheel.objects.get(id=fusion_wheel)
        clear = ClearWheel.objects.get(id=clear_wheel)
        track = SpinTrack.objects.get(id=spin_track)
        tipBey = Tip.objects.get(id=tip)
        tipeBey = Tipe.objects.get(id=tipe)

        Beyblade.objects.create(
            nombre=nombre, 
            descripcion=descripcion,
            fusion_wheel=fusion, 
            clear_wheel=clear, 
            spin_track=track, 
            tip=tipBey, 
            tipe=tipeBey, 
            photo=image,
            color=color,
            season=season,
            sistem=sistem
        )

        return Response(
            {"success": "El Beyblade ha sido agregado correctamente"},
            status=status.HTTP_201_CREATED
        )

    except (FusionWheel.DoesNotExist, ClearWheel.DoesNotExist, SpinTrack.DoesNotExist, Tip.DoesNotExist, Tipe.DoesNotExist):
        return Response(
            {"error": "Uno o más componentes no existen"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Error al crear beyblade: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(["POST"])
def crear_pieza(request):
    data = json.loads(request.body)
    tipo_pieza = data.get("tipo")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not tipo_pieza or not nombre or not descripcion:
        return Response(
            {"error", "Falta uno o más valores necesarios"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        if tipo_pieza == "fusion":
            FusionWheel.objects.create(nombre = nombre, descripcion=descripcion)

        elif tipo_pieza == "clear":
            ClearWheel.objects.create(nombre = nombre, descripcion=descripcion)

            return Response(
                {"success": "Se ha creado la rueda de energía exitosamente"},
                status=status.HTTP_201_CREATED
            )
        elif tipo_pieza == "track":
            SpinTrack.objects.create(nombre = nombre, descripcion=descripcion)

        elif tipo_pieza == "tip":
            Tip.objects.create(nombre = nombre, descripcion=descripcion)

        elif tipo_pieza == "tipe":
            Tipe.objects.create(nombre = nombre, descripcion=descripcion)

        else:
            return Response(
                {"error": "No se ha especificado el valor de pieza"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"success": "Se ha creado la pieza con exito"},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
         return Response(
             {"error": f"Se produjo un error al validar los datos enviados: {e}"},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
    
@api_view(["GET"])
def cargar_pieza(request):
    pieza = request.query_params.get("pieza")

    modelos = {
        "fusion": FusionWheel,
        "clear": ClearWheel,
        "track": SpinTrack,
        "tip": Tip,
        "tipe": Tipe
    }

    data = []

    if pieza in modelos:
        objetos = modelos[pieza].objects.all()

        for obj in objetos:
            data.append({
                "id": obj.id,
                "nombre": obj.nombre,
                "descripcion": obj.descripcion
            })
    else:
        for modelo in modelos.values():
            objetos = modelo.objects.all()

            for obj in objetos:
                data.append({
                    "id": obj.id,
                    "nombre": obj.nombre,
                    "descripcion": obj.descripcion
                })

    return Response(data)





@api_view(["GET"])
def cargar_fusion(request):
    fusions = FusionWheel.objects.all()

    data = []

    for f in fusions:

        list = {
            "id": f.id,
            "nombre": f.nombre,
            "descripcion": f.descripcion
        }
        data.append(list)
    
    return Response(data)
@api_view(["GET"])
def cargar_clear(request):
    clears = ClearWheel.objects.all()

    data = []

    for f in clears:

        list = {
            "id": f.id,
            "nombre": f.nombre,
            "descripcion": f.descripcion
        }
        data.append(list)
    
    return Response(data)
@api_view(["GET"])
def cargar_track(request):
    tracks = SpinTrack.objects.all()

    data = []

    for f in tracks:

        list = {
            "id": f.id,
            "nombre": f.nombre,
            "descripcion": f.descripcion
        }
        data.append(list)
    
    return Response(data)
@api_view(["GET"])
def cargar_tip(request):
    tips = Tip.objects.all()

    data = []

    for f in tips:

        list = {
            "id": f.id,
            "nombre": f.nombre,
            "descripcion": f.descripcion
        }
        data.append(list)
    
    return Response(data)
@api_view(["GET"])
def cargar_tipe(request):
    tipes = Tipe.objects.all()

    data = []

    for f in tipes:

        list = {
            "id": f.id,
            "nombre": f.nombre,
            "descripcion": f.descripcion
        }
        data.append(list)
    
    return Response(data)

@api_view(["GET"])
def cargar_beyblades(request):
    seleccion = request.query_params.get("select")
    
    if seleccion:
        bey = Beyblade.objects.filter(season__icontains = seleccion)
    else:
        bey = Beyblade.objects.all()

    data = []

    for i in bey:
        lista = {
            "id": i.id,
            "nombre": i.nombre,
            "photo": _get_image_url(i.photo),
            "color": i.color,
            "season": i.season
        }
        data.append(lista)
        
    return Response(data)

@api_view(["GET"])
def cargar_bey(request, pk):
    try:
        bey = Beyblade.objects.get(pk=pk)
    except Beyblade.DoesNotExist:
        return Response(
            {"error": "El beyblade no existe"},
            status = status.HTTP_404_NOT_FOUND
        )
    
    data = {
        "id": bey.id,
        "nombre": bey.nombre,
        "descripcion": bey.descripcion,
        "photo": _get_image_url(bey.photo),
        "fusion": bey.fusion_wheel.nombre,
        "fusion_id": bey.fusion_wheel.id if bey.fusion_wheel else None,
        "descripcion1": bey.fusion_wheel.descripcion if bey.fusion_wheel else "",
        "clear": bey.clear_wheel.nombre,
        "clear_id": bey.clear_wheel.id if bey.clear_wheel else None,
        "descripcion2": bey.clear_wheel.descripcion if bey.clear_wheel else "",
        "track": bey.spin_track.nombre,
        "track_id": bey.spin_track.id if bey.spin_track else None,
        "descripcion3": bey.spin_track.descripcion if bey.spin_track else "",
        "tip": bey.tip.nombre,
        "tip_id": bey.tip.id if bey.tip else None,
        "descripcion4": bey.tip.descripcion if bey.tip else "",
        "tipe": bey.tipe.nombre,
        "tipe_id": bey.tipe.id if bey.tipe else None,
        "descripcion5": bey.tipe.descripcion if bey.tipe else "",
        "color": bey.color,
        "season": bey.season,
        "sistem": bey.sistem
    }

    return Response(data, status = status.HTTP_200_OK)


@api_view(["PUT", "POST"])
def editar_beyblade(request, pk):
    try:
        try:
            bey = Beyblade.objects.get(pk=pk)
        except Beyblade.DoesNotExist:
            return Response({"error": "El beyblade no existe"}, status=status.HTTP_404_NOT_FOUND)

        if request.content_type == 'application/json':
            data = json.loads(request.body)
            nombre = data.get("nombre", bey.nombre)
            descripcion = data.get("descripcion", bey.descripcion)
            fusion_id = data.get("fusion")
            clear_id = data.get("clear")
            track_id = data.get("track")
            tip_id = data.get("tip")
            tipe_id = data.get("tipe")
            color = data.get("color", bey.color)
            season = data.get("season", bey.season)
            sistem = data.get("sistem", bey.sistem)
        else:
            nombre = request.POST.get("nombre", bey.nombre)
            descripcion = request.POST.get("descripcion", bey.descripcion)
            fusion_id = request.POST.get("fusion")
            clear_id = request.POST.get("clear")
            track_id = request.POST.get("track")
            tip_id = request.POST.get("tip")
            tipe_id = request.POST.get("tipe")
            color = request.POST.get("color", bey.color)
            season = request.POST.get("season", bey.season)
            sistem = request.POST.get("sistem", bey.sistem)

            if 'image' in request.FILES:
                image_file = request.FILES.get("image")
                if image_file:
                    try:
                        upload_result = cloudinary.uploader.upload(image_file, folder="beyblades")
                        bey.photo = upload_result.get("secure_url") or upload_result.get("url")
                    except Exception as cloud_err:
                        print(f"Error subiendo beyblade a Cloudinary: {cloud_err}")
                        bey.photo = image_file

        bey.nombre = nombre
        bey.descripcion = descripcion
        if color:
            bey.color = color
        if season:
            bey.season = season
        if sistem:
            bey.sistem = sistem

        if fusion_id:
            bey.fusion_wheel = FusionWheel.objects.get(id=fusion_id)
        if clear_id:
            bey.clear_wheel = ClearWheel.objects.get(id=clear_id)
        if track_id:
            bey.spin_track = SpinTrack.objects.get(id=track_id)
        if tip_id:
            bey.tip = Tip.objects.get(id=tip_id)
        if tipe_id:
            bey.tipe = Tipe.objects.get(id=tipe_id)

        bey.save()
        return Response({"success": "Beyblade actualizado con éxito"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al editar beyblade: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def eliminar_bey(request, pk):

    try:
        bey = Beyblade.objects.get(pk=pk)
    except Beyblade.DoesNotExist:
        return Response(
            {"error": "El beyblade seleccionado no existe"},
            status = status.HTTP_404_NOT_FOUND
        )
    
    bey.delete()

    return Response(
        {"success": "El beyblade fue eliminado con exito"},
        status = status.HTTP_200_OK
    )

@api_view([("GET")])
def buscador(request):
    busqueda = request.query_params.get("busqueda")

    
    resultados = Beyblade.objects.filter(nombre__icontains=busqueda)

    if not resultados.exists():
        pass

    resultados = Beyblade.objects.filter(descripcion__icontains=busqueda)
    
    if not resultados.exists():
        return Response(
            [],
            {"mensaje": "No se encontraron resultados"},
            status=status.HTTP_200_OK
        )
    
    data = []
    for r in resultados:
        list = {
            "id": r.id,
            "nombre": r.nombre,
            "descripcion": r.descripcion,
            "photo": _get_image_url(r.photo),
            "fusion": r.fusion_wheel.nombre,
            "descripcion1": r.fusion_wheel.descripcion,
            "clear": r.clear_wheel.nombre,
            "descripcion2": r.clear_wheel.descripcion,
            "track": r.spin_track.nombre,
            "descripcion3": r.spin_track.descripcion,
            "tip": r.tip.nombre,
            "descripcion4": r.tip.descripcion,
            "tipe": r.tipe.nombre,
            "descripcion5": r.tipe.descripcion,
            "color": r.color
        }
        data.append(list)
    
    return Response(data, status = status.HTTP_200_OK)

    



