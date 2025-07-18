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
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404

from sap.views import referenciasPorAnio, telasPorReferencia, insumosPorReferencia, getModeloDetalle, searchPTCode
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







class FasesDeReferenciaAPIView(APIView):
    def get(self, request, collection_id, referencia_id, fasesSlug):
        logger.info(f"Django [FaseDetalleAPIView]: Solicitud GET para Fase: {fasesSlug}, Referencia: {referencia_id}, Colección: {collection_id}")

        data_for_phase = {}

        try:
            if fasesSlug == 'jo':
                # Lógica para la fase JO
                # Ejemplo: data_for_phase = get_data_for_jo_phase(referencia_id)
                data_for_phase = {"mensaje": f"Datos para la fase JO de la referencia {referencia_id}"}

            elif fasesSlug == 'md-creacion-ficha':
                logger.info(f"Cargando datos para la fase 'MD Creacion Ficha' de la referencia {referencia_id} (Colección: {collection_id})")
                
                # *** LLAMAR A LAS FUNCIONES PASANDO collection_id directamente ***
                telas_data = telasPorReferencia(request, referencia_id, collection_id)     # <--- Pasa collection_id
                insumos_data = insumosPorReferencia(request, referencia_id, collection_id) # <--- Pasa collection_id

                data_for_phase = {
                    "mensaje": f"Datos de BD para MD Creacion Ficha de {referencia_id} (Colección: {collection_id})",
                    "telas": telas_data,
                    "insumos": insumos_data,
                }

            elif fasesSlug == 'md-creativo':
                # Lógica para la fase MD Creación Ficha
                data_for_phase = {"mensaje": f"Datos para la fase MD Creativo de la referencia {referencia_id}"}

            elif fasesSlug == 'md-corte':
                # Lógica para la fase MD Corte
                data_for_phase = {"mensaje": f"Datos para la fase MD Corte de la referencia {referencia_id}"}

            elif fasesSlug == 'md-confeccion':
                # Lógica para la fase MD Confección
                data_for_phase = {"mensaje": f"Datos para la fase MD Confección de la referencia {referencia_id}"}

            elif fasesSlug == 'md-fitting':
                # Lógica para la fase MD Fitting
                data_for_phase = {"mensaje": f"Datos para la fase MD Fitting de la referencia {referencia_id}"}

            elif fasesSlug == 'md-tecnico':     
                # Lógica para la fase MD Técnico
                data_for_phase = {"mensaje": f"Datos para la fase MD Técnico de la referencia {referencia_id}"}

            elif fasesSlug == 'md-trazador':
                # Lógica para la fase MD Trazador
                data_for_phase = {"mensaje": f"Datos para la fase MD Trazador de la referencia {referencia_id}"} 

            elif fasesSlug == 'costeo':
                data_for_phase = {"mensaje": f"Datos de COSTEO para la referencia {referencia_id}"}

            elif fasesSlug == 'pt-tecnico':
                # Lógica para la fase PT Técnico
                data_for_phase = {"mensaje": f"Datos para la fase PT Técnico de la referencia {referencia_id}"}  

            elif fasesSlug == 'pt-fitting':
                # Lógica para la fase PT Fitting
                data_for_phase = {"mensaje": f"Datos para la fase PT Fitting de la referencia {referencia_id}"}

            elif fasesSlug == 'pt-cortador':
                # Lógica para la fase PT Cortador
                data_for_phase = {"mensaje": f"Datos para la fase PT Cortador de la referencia {referencia_id}"} 

            elif fasesSlug == 'pt-trazador':
                # Lógica para la fase PT Trazador
                data_for_phase = {"mensaje": f"Datos para la fase PT Trazador de la referencia {referencia_id}"} 

            else:
                logger.warning(f"Fase '{fasesSlug}' no reconocida para la referencia {referencia_id}.")
                return Response({'detail': f'Fase "{fasesSlug}" no válida.'}, status=status.HTTP_404_NOT_FOUND)

            logger.info(f"Datos generados para {fasesSlug} de {referencia_id} (Colección: {collection_id}): {data_for_phase}")
            return Response(data_for_phase, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Django [FaseDetalleAPIView]: ERROR al obtener datos para fase '{fasesSlug}' de referencia '{referencia_id}' (Colección: {collection_id}): {e}", exc_info=True)
            return Response({'detail': f'Error al obtener datos de la fase: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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
        logger.info(f"Django [ModeloDetalleAPIView]: Solicitud GET recibida para referencia_id: {referencia_id}, - Colección ID: {request.GET.get('collectionId')}")
        try:
            # Llama a la función combinada que obtiene telas e insumos Y las fases
            combined_data = getModeloDetalle(request, referencia_id)

            # Puedes hacer una validación adicional aquí si combined_data es incompleto
            # if not combined_data.get('fases_disponibles'):
            #     logger.warning(f"Referencia {referencia_id} devuelta sin fases_disponibles.")
            #     return Response({'detail': 'Datos de referencia incompletos: faltan fases.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(combined_data, status=status.HTTP_200_OK)
        except ValueError as ve: # Captura el error específico si la referencia no se encuentra
            logger.error(f"Django [ModeloDetalleAPIView]: Referencia no encontrada '{referencia_id}': {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Django [ModeloDetalleAPIView]: ERROR al obtener el detalle del modelo para la referencia '{referencia_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener detalle del modelo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       


# apps/costeo_app/views.py (Fragmento relevante)

# ...
class FaseDetalleAPIView(APIView):
    def get(self, request, collection_id, referencia_id, fasesSlug):
        # ...
        if fasesSlug == 'md-creacion-ficha':
            telas_data = telasPorReferencia(request, referencia_id, collection_id)
            insumos_data = insumosPorReferencia(request, referencia_id, collection_id)

            data_for_phase = {
                "mensaje": f"Datos de BD para MD Creacion Ficha de {referencia_id} (Colección: {collection_id})",
                "telas": telas_data,     # <--- Asegúrate que esto es un array de objetos
                "insumos": insumos_data, # <--- Asegúrate que esto es un array de objetos
            }
        # ...
        return Response(data_for_phase, status=status.HTTP_200_OK)



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


# class ProductoListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer

# class CollectionCreateView(generics.CreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

# class TecnicoViewSet(viewsets.ModelViewSet):
#     queryset = Tecnico.objects.all()
#     serializer_class = TecnicoSerializer

# class TelaViewSet(viewsets.ModelViewSet):
#     queryset = Tela.objects.all()
#     serializer_class = TelaSerializer

# class CreativoViewSet(viewsets.ModelViewSet):
#     queryset = Creativo.objects.all()
#     serializer_class = CreativoSerializer



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
