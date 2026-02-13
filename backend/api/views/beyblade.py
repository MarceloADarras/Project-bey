from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F
from django.db import IntegrityError
from rest_framework.views import APIView
from api.models import Beyblade, FusionWheel, ClearWheel, SpinTrack, Tip, Tipe
import json


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
        color = request.POST.get("color")
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
        image = request.FILES.get("image") if 'image' in request.FILES else None

    # Validate required fields
    if not all([nombre, descripcion, fusion_wheel, clear_wheel, spin_track, tip, tipe, color]):
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
            color=color
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
def crear_fusion(request):
    data = json.loads(request.body)
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    FusionWheel.objects.create(nombre = nombre, descripcion=descripcion)

    return Response(
        {"success": "Se ha creado la rueda de fusión exitosamente"},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
def crear_clear(request):
    data = json.loads(request.body)
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    ClearWheel.objects.create(nombre = nombre, descripcion=descripcion)

    return Response(
        {"success": "Se ha creado la rueda de energía exitosamente"},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
def crear_track(request):
    data = json.loads(request.body)
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    SpinTrack.objects.create(nombre = nombre, descripcion=descripcion)

    return Response(
        {"success": "Se ha creado el eje de rotación exitosamente"},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
def crear_tip(request):
    data = json.loads(request.body)
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    Tip.objects.create(nombre = nombre, descripcion=descripcion)

    return Response(
        {"success": "Se ha creado la punta de rendimiento exitosamente"},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
def crear_tipe(request):
    data = json.loads(request.body)
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    Tipe.objects.create(nombre = nombre, descripcion=descripcion)

    return Response(
        {"success": "Se ha creado el tipo exitosamente"},
        status=status.HTTP_201_CREATED
    )

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
    bey = Beyblade.objects.all()

    data = []

    for i in bey:
        lista = {
            "id": i.id,
            "nombre": i.nombre,
            "photo": i.photo.url if i.photo else None,
            "color": i.color
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
        "photo": bey.photo.url if bey.photo else None,
        "fusion": bey.fusion_wheel.nombre,
        "descripcion1": bey.fusion_wheel.descripcion,
        "clear": bey.clear_wheel.nombre,
        "descripcion2": bey.clear_wheel.descripcion,
        "track": bey.spin_track.nombre,
        "descripcion3": bey.spin_track.descripcion,
        "tip": bey.tip.nombre,
        "descripcion4": bey.tip.descripcion,
        "tipe": bey.tipe.nombre,
        "descripcion5": bey.tipe.descripcion,
        "color": bey.color
    }

    return Response(data, status = status.HTTP_200_OK)

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
            "photo": r.photo.url if r.photo else None,
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
    



