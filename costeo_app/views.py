from .models import Producto, Collection, Tela, Status
from .models import Foto, Creativo, Tecnico, ColorReferencia, Tipo, Variacion, Collection, Sublinea, Linea, LineaSublinea
from .forms import  CollectionForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductoSerializer, CollectionSerializer, TecnicoSerializer,TelaSerializer, CreativoSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from sap.views import modelsExample

        
@login_required
def index(request):    
    return render(request, "index.html")  
    
    # title = 'Django-Course!!'   
    # context = {
    #     'respuesta': 'Hola, soy Daniel, ¿en qué puedo ayudarte?',
    #     "nombre": 'Daniel',
    #     "apellido": 'Gossdfsdfsdfsfsdfez',
    # }
    # return JsonResponse(context, status=200, safe=False) 


def anio_coleccion(request, coleccion):
    coleccion_data = {
        # 'WINTER_SUN':['063','085','105'],
        # 'RESORT_RTW':['065','084','106'], 
        # 'SPRING_SUMMER':['067','088','110'],
        # 'SUMMER_VACATION':['070','088','111'],
        # 'PRE_FALL':['071','094','112'],
        # 'FALL_WINTER':['075','096','113'],
        # # 'CAPSULES':['071','091','114'],

        'WINTER_SUN': [
            {'id': '063', 'img': 'img/1.WINTER_SUN/Winter Sun 2024.png', 'bg': '#feea4d', 'label': '2024'},
            {'id': '085', 'img': 'img/1.WINTER_SUN/Winter Sun 2025.png', 'bg': '#feea4d', 'label': '2025'},
            {'id': '105', 'img': 'img/1.WINTER_SUN/Winter Sun 2026.png', 'bg': '#feea4d', 'label': '2026'},
        ],
        'RESORT_RTW': [
            {'id': '065', 'img': 'img/2.RESORT_RTW/Resort RTW 2024.png', 'bg': '#70a7ff', 'label': '2024'},
            {'id': '084', 'img': 'img/2.RESORT_RTW/Resort RTW 2025.png', 'bg': "#70a7ff", 'label': '2025'},
            {'id': '106', 'img': 'img/2.RESORT_RTW/Resort RTW 2026.png', 'bg': '#70a7ff', 'label': '2026'},
        ],
        'SPRING_SUMMER': [
            {'id': '067', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2024.png', 'bg': '#81c963', 'label': '2024'},
            {'id': '088', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2025.png', 'bg': '#81c963', 'label': '2025'},
            {'id': '110', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2026.png', 'bg': '#81c963', 'label': '2026'},
        ],
        'SUMMER_VACATION': [
            {'id': '070', 'img': 'img/4.SUMMER_VACATION/Summer Vacation 2024.png', 'bg': '#ff935f', 'label': '2024'},
            {'id': '088', 'img': 'img/4.SUMMER_VACATION/Summer Vacation 2025.png', 'bg': '#ff935f', 'label': '2025'},
            # {'id': '111', 'img': 'img/4.SUMMERVACATION/Summer Vacation 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
        'PRE_FALL': [
            {'id': '071', 'img': 'img/5.PRE_FALL/Pre Fall RTW 2024.png', 'bg': '#c6b9b1', 'label': '2024'},
            {'id': '094', 'img': 'img/5.PRE_FALL/Pre Fall RTW 2025.png', 'bg': '#c6b9b1', 'label': '2025'},
            # {'id': '112', 'img': 'img/5.PREFALL/Pre Fall 2026.png', 'bg': '#d4a5a5', 'label': '2026'},
        ],
        'FALL_WINTER': [
            {'id': '075', 'img': 'img/6.FALL_WINTER/Fall Winter 2024.png', 'bg': '#b03c5c', 'label': '2024'},
            {'id': '096', 'img': 'img/6.FALL_WINTER/Fall Winter 2025.png', 'bg': '#b03c5c', 'label': '2025'},
            # {'id': '113', 'img': 'img/6.FALLWINTER/Fall Winter 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
    }

    cards = coleccion_data.get(coleccion.upper(), [])

    context = {
        'coleccion': coleccion,
        'cards': cards,
    }
    return render(request, "colecciones/anio_coleccion.html", context)
    

    
def referencias(request, collection_id):   
    # id=request.GET.get('collection_id', collection_id)   
    # print("ID de colección:", id)

    data = modelsExample(request, collection_id)

    context = {
        "modelos": data[0:100],        
    }

    return render(request, "colecciones/referencias.html", context)


def obtener_sublineas(request, linea_id):
    sublineas = Sublinea.objects.filter(lineasublinea__linea_id=linea_id)
    data = [
        {"id": s.id, "nombre_sublinea": s.nombre_sublinea}
        for s in sublineas
    ]
    return JsonResponse(data, safe=False)


def collection_list(request):
    coleccion = Collection.objects.all()
    #print(coleccion.values())
    return render(request, 'colecciones/colecciones.html',{
        'miColeccion': coleccion,
    })


def create_reference(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all()
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()
    codigo_color = ColorReferencia.objects.all()
    linea = Linea.objects.all()
    sublinea = Sublinea.objects.all()
    lineaSublinea = LineaSublinea.objects.all()
    color_ref = ColorReferencia.objects.all()

    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        print(
            request.POST.get('referencia'),
            request.POST.get('foto_referencia'),
            request.POST.get('nombre_sistema'),
            request.POST.get('codigo_sap_md'),
            request.POST.get('codigo_sap_pt'),
            request.POST.get('descripcion_color'),
            request.POST.get('creativo'),
            request.POST.get('tecnico'),
            request.POST.get('status'),
            request.POST.get('codigo_color'),
            request.POST.get('linea'),
            request.POST.get('lineasublinea'),
        )
        if form.is_valid():
            form.save()
            return redirect('collection')
    else:
        form = CollectionForm()

    return render(request, 'colecciones/create.html', {
        'form': form,
        'miCreativo': creativo,
        'miTecnico': tecnico,
        'miStatus': status,
        'miTipo': tipo,
        'miVariacion': variacion,
        'miColorReferencia': codigo_color,
        'miLinea': linea,
        'miSublinea': sublinea,
        'miDescripcionRef': color_ref,
        'miLineaSublinea': lineaSublinea,
    })


def RegisterReference(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all()
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()

    if request.method == "POST":
        referencia = request.POST.get('referencia')
        nombre_referente = request.POST.get('nombre_referente')
        codigo_sap_md = request.POST.get('codigo_sap_md')
        codigo_sap_pt = request.POST.get('codigo_sap_pt')
        status_id = request.POST.get('status')
        creativo_id = request.POST.get('creativo')
        tecnico_id = request.POST.get('tecnico')
        tipo_id = request.POST.get('tipo')
        variacion_id = request.POST.get('variacion')
        linea_id = request.POST.get('linea')

        print(referencia, nombre_referente, codigo_sap_md, codigo_sap_pt, status_id, creativo_id, tecnico_id, tipo_id, variacion_id, linea_id)

        foto_ref = request.FILES.get('foto')
        foto_referencia = None
        if foto_ref:
            fs = FileSystemStorage()
            filename = fs.save(foto_ref.name, foto_ref)
            uploaded_file_url = fs.url(filename)
            foto_referencia = Foto.objects.create(ruta_foto=uploaded_file_url)

        # Crear la nueva colección en la base de datos
        nueva_coleccion = Collection.objects.create(
            referencia=referencia,
            foto_referencia=foto_referencia,
            codigo_sap_md=codigo_sap_md,
            codigo_sap_pt=codigo_sap_pt,
            nombre_referente=nombre_referente,
            status_id=status_id,
            creativo_id=creativo_id,
            tecnico_id=tecnico_id,
            linea_id=linea_id,
        )
        return redirect('RegisterReference')

    return render(request, 'colecciones/register_ref.html', {
        'miStatus': status,
        'miCreativo': creativo,
        'miTecnico': tecnico,
        'miTipo': tipo,
        'miVariacion': variacion,
    })


def about(request):
    return render(request, "about.html")


def signout(request):
    logout(request)
    print('Salir de la sesión')
    return redirect('signin')




class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CollectionCreateView(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer

class TelaViewSet(viewsets.ModelViewSet):
    queryset = Tela.objects.all()
    serializer_class = TelaSerializer

class CreativoViewSet(viewsets.ModelViewSet):
    queryset = Creativo.objects.all()
    serializer_class = CreativoSerializer



@api_view(['GET'])
def lista_coleccion(request):
    nombre = request.GET.get('nombre')
    # Simulación básica
    data = [
        {'producto': 'Vestido largo', 'coleccion': nombre},
        {'producto': 'Chaqueta de cuero', 'coleccion': nombre},
    ]
    return Response(data)


class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "¡Estos son datos protegidos, " + request.user.username + "!"})
