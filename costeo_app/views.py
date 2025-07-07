from .models import Producto, Collection, Tela, Status, Referencia
from .models import Foto, Creativo, Tecnico, ColorReferencia, Tipo, Variacion, Collection, Sublinea, Linea, LineaSublinea
from .forms import  CollectionForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductoSerializer, CollectionSerializer, TecnicoSerializer,TelaSerializer, CreativoSerializer, ReferenciaSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from sap.views import referenciasPorAnio, telasPorReferencia, insumosPorReferencia, getModeloDetalle, searchPTCode
from rest_framework.views import APIView
from django.http import Http404

import logging


logger = logging.getLogger(__name__)


class AnioColeccionAPIView(APIView):
    def get(self, request, coleccion): # 'coleccion' será el slug de Next.js (ej. "winter-sun")
        print(f"Django [AnioColeccionAPIView]: Slug recibido: '{coleccion}'")
        nombre_legible = {
            'winter-sun': 'Winter Sun',
            'resort-rtw': 'Resort RTW',
            'spring-summer': 'Spring Summer',
            'summer-vacation': 'Summer Vacation',
            'pre-fall': 'Pre Fall RTW',
            'fall-winter': 'Fall Winter',
        }

        coleccion_data = {
            'winter-sun': [
                {'id': '063', 'img': '/img/1.WINTER_SUN/Winter Sun 2024.png', 'bg': '#feea4d', 'label': '2024'},
                {'id': '085', 'img': '/img/1.WINTER_SUN/Winter Sun 2025.png', 'bg': '#feea4d', 'label': '2025'},
                {'id': '105', 'img': '/img/1.WINTER_SUN/Winter Sun 2026.png', 'bg': '#feea4d', 'label': '2026'},
            ],
            'resort-rtw': [
                {'id': '065', 'img': '/img/2.RESORT_RTW/Resort RTW 2024.png', 'bg': '#70a7ff', 'label': '2024'},
                {'id': '084', 'img': '/img/2.RESORT_RTW/Resort RTW 2025.png', 'bg': "#70a7ff", 'label': '2025'},
                {'id': '106', 'img': '/img/2.RESORT_RTW/Resort RTW 2026.png', 'bg': '#70a7ff', 'label': '2026'},
            ],
            'spring-summer': [
                {'id': '067', 'img': '/img/3.SPRING_SUMMER/Spring Summer 2024.png', 'bg': '#81c963', 'label': '2024'},
                {'id': '088', 'img': '/img/3.SPRING_SUMMER/Spring Summer 2025.png', 'bg': '#81c963', 'label': '2025'},
                {'id': '110', 'img': '/img/3.SPRING_SUMMER/Spring Summer 2026.png', 'bg': '#81c963', 'label': '2026'},
            ],
            'summer-vacation': [
                {'id': '070', 'img': '/img/4.SUMMER_VACATION/Summer Vacation 2024.png', 'bg': '#ff935f', 'label': '2024'},
                {'id': '094', 'img': '/img/4.SUMMER_VACATION/Summer Vacation 2025.png', 'bg': '#ff935f', 'label': '2025'},
            ],
            'pre-fall': [
                {'id': '071', 'img': '/img/5.PRE_FALL/Pre Fall RTW 2024.png', 'bg': '#c6b9b1', 'label': '2024'},
                {'id': '096', 'img': '/img/5.PRE_FALL/Pre Fall RTW 2025.png', 'bg': '#c6b9b1', 'label': '2025'},
            ],
            'fall-winter': [
                {'id': '075', 'img': '/img/6.FALL_WINTER/Fall Winter 2024.png', 'bg': '#b03c5c', 'label': '2024'},
                {'id': '102', 'img': '/img/6.FALL_WINTER/Fall Winter 2025.png', 'bg': '#b03c5c', 'label': '2025'},
            ],
        }
        # Busca la colección directamente con el slug recibido
        cards = coleccion_data.get(coleccion, [])

        if cards:
            print(f"Django [AnioColeccionAPIView]: Colección '{coleccion}' encontrada. Enviando {len(cards)} tarjetas.")
            return Response({
                'nombre_coleccion': nombre_legible.get(coleccion, coleccion),
                'anios': cards
            }, status=status.HTTP_200_OK)
        else:
            print(f"Django [AnioColeccionAPIView]: ERROR: Colección '{coleccion}' NO encontrada.")
            return Response({'detail': f'Colección "{coleccion}" no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        


class ReferenciasAnioAPIView(APIView):
    print("Django: [ReferenciasAPIView] Inicializando la vista para obtener referencias por año.")
    def get(self, request, collection_id):
        logger.info(f"Django [ReferenciasAPIView]: Solicitud GET recibida para collection_id: {collection_id}")
        try:
            # Llama a la función referenciasPorAno, que ahora devuelve una lista directamente
            data_from_db = referenciasPorAnio(collection_id)
            return Response(data_from_db, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Django [ReferenciasAPIView]: ERROR al obtener referencias para la colección '{collection_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener referencias: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ReferenciaDetailView(generics.RetrieveAPIView):
    # Ya no necesitas queryset si vas a sobrescribir get_object completamente para simulación
    # queryset = Referencia.objects.all()
    serializer_class = ReferenciaSerializer
    lookup_field = 'codigo_referencia' # Esto DEBE coincidir con el nombre del parámetro en la URL

    def get_object(self):
        # La forma correcta y robusta de obtener el valor del lookup_field
        # self.kwargs es el diccionario de argumentos capturados por la URL
        # self.lookup_field es el nombre de la clave que esperamos ('codigo_referencia')
        try:
            codigo_referencia = self.kwargs[self.lookup_field] # Esta es la línea 31
        except KeyError:
            # Esto NO debería ocurrir si la URL está bien configurada
            raise Http404(f"La URL no proporcionó el parámetro esperado '{self.lookup_field}'.")

        # --- SIMULACIÓN DE DATOS REVISADA ---
        if codigo_referencia == "PT01660":
            referencia = Referencia(
                codigo_referencia="PT01660",
                nombre="Chaqueta Casual Urbana",
                imagen_url="http://localhost:8000/media/referencias/chaqueta_ejemplo.jpg"
            )
            return referencia
        elif codigo_referencia == "PT00001":
            referencia = Referencia(
                codigo_referencia="PT00001",
                nombre="Vestido Noche Elegante",
                imagen_url="http://localhost:8000/media/referencias/vestido_ejemplo.jpg"
            )
            return referencia
        else:
            # Si no es un ID simulado, intenta buscar en la base de datos real
            # (Si no tienes datos reales en DB, esto lanzará otro Http404)
            # Descomenta la siguiente línea SI planeas tener datos reales en tu DB para Referencia.
            # return super().get_object()
            raise Http404(f"Referencia con código '{codigo_referencia}' no encontrada en la simulación.")





#---------------------------------------------------------------------------------------------
class TestDataAPIView(APIView):
    def get(self, request, test_id): # 'test_id' es el parámetro de la URL
        print(f"Django: [TestDataAPIView] Recibida solicitud para test_id: {test_id}") # Log en la terminal de Django
        
        data = {
            'id': test_id,
            'message': f'¡Datos recibidos con éxito para el ID de prueba: {test_id}!',
            'source': 'Django Backend',
            'timestamp': '2024-06-25T10:00:00Z' # Un dato fijo para probar
        }
        
        print(f"Django: [TestDataAPIView] Enviando respuesta: {data}") # Log en la terminal de Django
        return Response(data, status=status.HTTP_200_OK)







  

# --- NUEVA APIView COMBINADA ---

class ModeloDetalleAPIView(APIView):
    def get(self, request, referencia_id):
        logger.info(f"Django [ModeloDetalleAPIView]: Solicitud GET recibida para referencia_id: {referencia_id}")
        try:
            # Llama a la función combinada que obtiene telas e insumos
            combined_data = getModeloDetalle(request, referencia_id)
            return Response(combined_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Django [ModeloDetalleAPIView]: ERROR al obtener el detalle del modelo para la referencia '{referencia_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener detalle del modelo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#NUEVA APIView para obtener el detalle del modelo
class ModeloDetalleAPIView(APIView):
    def get(self, request, referencia_id):
        logger.info(f"Django [ModeloDetalleAPIView]: Solicitud GET recibida para referencia_id: {referencia_id}")
        try:
            combined_data = getModeloDetalle(request, referencia_id)
            return Response(combined_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Django [ModeloDetalleAPIView]: ERROR al obtener el detalle del modelo para la referencia '{referencia_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener detalle del modelo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# NUEVA APIView para la búsqueda de PT Code
class PTSearchAPIView(APIView):
    def get(self, request):
        pt_code = request.GET.get('ptCode', '').strip() # Obtiene el ptCode de los query parameters
        logger.info(f"Django [PTSearchAPIView]: Solicitud GET recibida para búsqueda de PT Code: {pt_code}")

        if not pt_code:
            return Response({'detail': 'Parámetro "ptCode" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Llama a la función de lógica de negocio para buscar el PT Code
            # Esta función devolverá el primer resultado encontrado (PT Code y Collection)
            search_result = searchPTCode(pt_code)

            if search_result:
                return Response(search_result, status=status.HTTP_200_OK)
            else:
                return Response({'detail': f"Código PT '{pt_code}' no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Django [PTSearchAPIView]: ERROR al buscar PT Code '{pt_code}': {e}", exc_info=True)
            return Response({'detail': f'Error al realizar la búsqueda: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






#   ------- D J A N G O   V I E W S / T E M P L A T E S  -------

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
    print("Django: ", coleccion)
    coleccion_data = {       

        'winter-sun': [
            {'id': '063', 'img': 'img/1.WINTER_SUN/Winter Sun 2024.png', 'bg': '#feea4d', 'label': '2024'},
            {'id': '085', 'img': 'img/1.WINTER_SUN/Winter Sun 2025.png', 'bg': '#feea4d', 'label': '2025'},
            {'id': '105', 'img': 'img/1.WINTER_SUN/Winter Sun 2026.png', 'bg': '#feea4d', 'label': '2026'},
        ],
        'resort-rtw': [
            {'id': '065', 'img': 'img/2.RESORT_RTW/Resort RTW 2024.png', 'bg': '#70a7ff', 'label': '2024'},
            {'id': '084', 'img': 'img/2.RESORT_RTW/Resort RTW 2025.png', 'bg': "#70a7ff", 'label': '2025'},
            {'id': '106', 'img': 'img/2.RESORT_RTW/Resort RTW 2026.png', 'bg': '#70a7ff', 'label': '2026'},
        ],
        'spring-summer': [
            {'id': '067', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2024.png', 'bg': '#81c963', 'label': '2024'},
            {'id': '088', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2025.png', 'bg': '#81c963', 'label': '2025'},
            {'id': '110', 'img': 'img/3.SPRING_SUMMER/Spring Summer 2026.png', 'bg': '#81c963', 'label': '2026'},
        ],
        'summer-vacation': [
            {'id': '070', 'img': 'img/4.SUMMER_VACATION/Summer Vacation 2024.png', 'bg': '#ff935f', 'label': '2024'},
            {'id': '094', 'img': 'img/4.SUMMER_VACATION/Summer Vacation 2025.png', 'bg': '#ff935f', 'label': '2025'},
            # {'id': '111', 'img': 'img/4.SUMMERVACATION/Summer Vacation 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
        'pre-fall': [
            {'id': '071', 'img': 'img/5.PRE_FALL/Pre Fall RTW 2024.png', 'bg': '#c6b9b1', 'label': '2024'},
            {'id': '096', 'img': 'img/5.PRE_FALL/Pre Fall RTW 2025.png', 'bg': '#c6b9b1', 'label': '2025'},
            # {'id': '112', 'img': 'img/5.PREFALL/Pre Fall 2026.png', 'bg': '#d4a5a5', 'label': '2026'},
        ],
        'fall-winter': [
            {'id': '075', 'img': 'img/6.FALL_WINTER/Fall Winter 2024.png', 'bg': '#b03c5c', 'label': '2024'},
            {'id': '102', 'img': 'img/6.FALL_WINTER/Fall Winter 2025.png', 'bg': '#b03c5c', 'label': '2025'},
            # {'id': '113', 'img': 'img/6.FALLWINTER/Fall Winter 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
    }
    cards = coleccion_data.get(coleccion, [])
    context = {
        'coleccion': coleccion,
        'cards': cards,
    }
    return render(request, "colecciones/anio_coleccion.html", context)





def referencias(request, collection_id):   
    # id=request.GET.get('collection_id', collection_id)   
    # print("ID de colección:", id)
    print("JEFERSON: ",collection_id)

    data = referenciasPorAnio(request, collection_id)

    context = {        
        "modelos": data[:],     #CANTIDAD DE CARDS QUE QUE GENERAN [0:100]      
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
