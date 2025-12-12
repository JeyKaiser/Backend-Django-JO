from .models import Producto, Collection, Tela, Status
from .models import (Foto, Creativo, Tecnico, ColorReferencia, Tipo, Variacion, Collection, Sublinea, Linea, LineaSublinea,
                     DimPrenda, DimCantidadTelas, DimUsoTela, DimBaseTextil,
                     DimCaracteristicaColor, DimAnchoUtil, DimPropiedadesTela,
                     DimVariante, DimDescripcion, DimTerminacion, FactConsumo)
from .serializers import (ProductoSerializer, CollectionSerializer, TecnicoSerializer, TelaSerializer, CreativoSerializer,
                          DimPrendaSerializer, DimCantidadTelasSerializer, DimUsoTelaSerializer, DimBaseTextilSerializer,
                          DimCaracteristicaColorSerializer, DimAnchoUtilSerializer, DimPropiedadesTelaSerializer,
                          DimVarianteSerializer, DimDescripcionSerializer, DimTerminacionSerializer, FactConsumoSerializer)
from .forms import  CollectionForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404

from sap_app.hana_services import (
    get_collections_service,
    create_collection_service,
    get_traceability_service,
    update_traceability_service,
    get_current_traceability_service,
    get_phase_by_code_service,
    get_all_phases_service,
    get_reference_detail_service,
    search_reference_service,
    get_references_by_year_service,
    get_telas_por_referencia_service,
    get_insumos_por_referencia_service
)
import logging


logger = logging.getLogger(__name__)

def get_season_details(name):
    name_upper = name.upper()
    if 'WINTER SUN' in name_upper:
        return 'Winter Sun', '#feea4d', '1.WINTER_SUN'
    if 'RESORT' in name_upper:
        return 'Resort RTW', '#70a7ff', '2.RESORT_RTW'
    if 'SPRING SUMMER' in name_upper:
        return 'Spring Summer', '#81c963', '3.SPRING_SUMMER'
    if 'SUMMER VACATION' in name_upper:
        return 'Summer Vacation', '#ff935f', '4.SUMMER_VACATION'
    if 'PREFALL' in name_upper:
        return 'Pre Fall RTW', '#c6b9b1', '5.PRE_FALL'
    if 'FALL WINTER' in name_upper:
        return 'Fall Winter', '#b03c5c', '6.FALL_WINTER'
    return 'Unknown', '#ffffff', 'default'

class ColeccionesAPIView(APIView):
    def get(self, request):
        print("Django [ColeccionesAPIView]: Solicitud GET recibida para obtener todas las colecciones desde HANA")
        
        data_from_db, error = get_collections_service()

        if error:
            logger.error(f"Django [ColeccionesAPIView]: Error de base de datos: {error}")
            return Response({"detail": f"Error de base de datos: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        colecciones = []
        if data_from_db:
            for item in data_from_db:
                name = item.get('Name')
                year = item.get('U_GSP_SEASON')
                
                season, bg_color, img_folder = get_season_details(name)

                coleccion = {
                    'id': str(year) if year else 'unknown',
                    'label': name,
                    'img': f'/img/{img_folder}/{name}.png',
                    'bg': bg_color,
                    'status': 'active',
                    'season': season,
                    'year': str(year) if year else 'N/A',
                    'lastUpdated': 'N/A'
                }
                colecciones.append(coleccion)
            
        print(f"Django [ColeccionesAPIView]: Enviando {len(colecciones)} colecciones desde HANA")
        return Response(colecciones, status=status.HTTP_200_OK)

    def post(self, request):
        print("Django [ColeccionesAPIView]: Solicitud POST recibida para crear una colección")
        
        data = request.data
        code = data.get('Code')
        name = data.get('Name')
        season = data.get('U_GSP_SEASON')

        if not all([code, name, season]):
            return Response(
                {"detail": "Missing required fields: Code, Name, U_GSP_SEASON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        error = create_collection_service(code, name, season)

        if error:
            logger.error(f"Django [ColeccionesAPIView]: Error de base de datos al crear colección: {error}")
            return Response(
                {"detail": f"Error de base de datos: {error}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"message": "Collection created successfully"},
            status=status.HTTP_201_CREATED
        )

class TrazabilidadAPIView(APIView):
    def get(self, request, id_referencia):
        logger.info(f"Django [TrazabilidadAPIView]: Solicitud GET recibida para la trazabilidad de la referencia con ID: {id_referencia}")
        
        data_from_db, error = get_traceability_service(id_referencia)
        
        if error:
            logger.error(f"Django [TrazabilidadAPIView]: Error de base de datos: {error}")
            return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data_from_db, status=status.HTTP_200_OK)

    def post(self, request, id_referencia):
        data = request.data
        id_fase = data.get('ID_FASE')
        
        error = update_traceability_service(id_fase, id_referencia)
        
        if error:
            logger.error(f"Django [TrazabilidadAPIView]: Error de base de datos: {error}")
            return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Traceability record created successfully'}, status=status.HTTP_201_CREATED)

class TrazabilidadCurrentAPIView(APIView):
    def get(self, request, id_referencia):
        logger.info(f"Django [TrazabilidadCurrentAPIView]: Solicitud GET recibida para la fase actual de la referencia con ID: {id_referencia}")
        
        data_from_db, error = get_current_traceability_service(id_referencia)
        
        if error:
            logger.error(f"Django [TrazabilidadCurrentAPIView]: Error de base de datos: {error}")
            return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not data_from_db:
            return Response({'detail': 'Current phase not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data_from_db[0], status=status.HTTP_200_OK)

class FasesAPIView(APIView):
    def get(self, request, codigo_fase=None):
        if codigo_fase:
            logger.info(f"Django [FasesAPIView]: Solicitud GET recibida para la fase con código: {codigo_fase}")
            
            data_from_db, error = get_phase_by_code_service(codigo_fase)
            
            if error:
                logger.error(f"Django [FasesAPIView]: Error de base de datos: {error}")
                return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not data_from_db:
                return Response({'detail': 'Phase not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data_from_db[0], status=status.HTTP_200_OK)
        else:
            logger.info(f"Django [FasesAPIView]: Solicitud GET recibida para obtener todas las fases")
            
            data_from_db, error = get_all_phases_service()
            
            if error:
                logger.error(f"Django [FasesAPIView]: Error de base de datos: {error}")
                return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(data_from_db, status=status.HTTP_200_OK)


class ReferenciaDetalleAPIView(APIView):
    def get(self, request, codigo_referencia):
        logger.info(f"Django [ReferenciaDetalleAPIView]: Solicitud GET recibida para codigo_referencia: {codigo_referencia}")
        
        data_from_db, error = get_reference_detail_service(codigo_referencia)
        
        if error:
            logger.error(f"Django [ReferenciaDetalleAPIView]: Error de base de datos: {error}")
            return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not data_from_db:
            return Response({'detail': 'Reference not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data_from_db[0], status=status.HTTP_200_OK)

class ReferenciaSearchAPIView(APIView):
    def get(self, request):
        search_term = request.query_params.get('search', '')
        
        data_from_db, error = search_reference_service(search_term)
        
        if error:
            logger.error(f"Django [ReferenciaSearchAPIView]: Error de base de datos: {error}")
            return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data_from_db, status=status.HTTP_200_OK)

    

class ReferenciasAnioAPIView(APIView):
    def get(self, request, collection_id):
        logger.info(f"Django [ReferenciasAPIView]: Solicitud GET recibida para collection_id: {collection_id}")
        
        try:
            data_from_db, error = get_references_by_year_service(collection_id)
            
            if error:
                logger.error(f"Django [ReferenciasAPIView]: Error de base de datos al obtener referencias para la colección '{collection_id}': {error}")
                return Response({'detail': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Devolviendo {len(data_from_db)} referencias para la colección {collection_id}")
            return Response(data_from_db, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Django [ReferenciasAPIView]: ERROR inesperado al obtener referencias para la colección '{collection_id}': {e}", exc_info=True)
            return Response({'detail': f'Error inesperado al obtener referencias: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








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
            fases_disponibles = [
                {'slug': 'jo', 'nombre': 'JO'},
                {'slug': 'md-creacion-ficha', 'nombre': 'MD - Creación Ficha'},
                {'slug': 'md-creativo', 'nombre': 'MD - Creativo'},
                {'slug': 'md-corte', 'nombre': 'MD - Corte'},
                {'slug': 'md-confeccion', 'nombre': 'MD - Confección'},
                {'slug': 'md-fitting', 'nombre': 'MD - Fitting'},
                {'slug': 'md-tecnico', 'nombre': 'MD - Técnico'},
                {'slug': 'md-trazador', 'nombre': 'MD - Trazador'},
                {'slug': 'costeo', 'nombre': 'Costeo'},
                {'slug': 'pt-tecnico', 'nombre': 'PT - Técnico'},
                {'slug': 'pt-fitting', 'nombre': 'PT - Fitting'},
                {'slug': 'pt-cortador', 'nombre': 'PT - Cortador'},
                {'slug': 'pt-trazador', 'nombre': 'PT - Trazador'},
            ]

            combined_data = {
                "referencia_id": referencia_id,
                "collection_id": request.GET.get('collectionId', ''),
                "telas": [],
                "insumos": [],
                "fases_disponibles": fases_disponibles
            }

            return Response(combined_data, status=status.HTTP_200_OK)
        except ValueError as ve:
            logger.error(f"Django [ModeloDetalleAPIView]: Referencia no encontrada '{referencia_id}': {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Django [ModeloDetalleAPIView]: ERROR al obtener el detalle del modelo para la referencia '{referencia_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener detalle del modelo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       







#   ------- D J A N G O   V I E W S / T E M P L A T E S  -------
def anio_coleccion(request, coleccion):
    print("Django: ", coleccion)
    coleccion_data = {       

        'winter-sun': [
            {'id': '063', 'img': 'img/1.WINTER_SUN/Winter Sun 2024.png', 'bg': '#feea4d', 'label': '2024'},
            {'id': '085', 'img': 'img/1.WINTER_SUN/Winter Sun 2025.png', 'bg': '#feea4d', 'label': '2025'},
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
            # {'id': '111', 'img': 'img/4.SUMMERVACATION/Summer Vacation 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
        'pre-fall': [
            {'id': '071', 'img': '/img/5.PRE_FALL/Pre Fall RTW 2024.png', 'bg': '#c6b9b1', 'label': '2024'},
            {'id': '096', 'img': '/img/5.PRE_FALL/Pre Fall RTW 2025.png', 'bg': '#c6b9b1', 'label': '2025'},
            # {'id': '112', 'img': 'img/5.PREFALL/Pre Fall 2026.png', 'bg': '#d4a5a5', 'label': '2026'},
        ],
        'fall-winter': [
            {'id': '075', 'img': '/img/6.FALL_WINTER/Fall Winter 2024.png', 'bg': '#b03c5c', 'label': '2024'},
            {'id': '102', 'img': '/img/6.FALL_WINTER/Fall Winter 2025.png', 'bg': '#b03c5c', 'label': '2025'},
            # {'id': '113', 'img': 'img/6.FALLWINTER/Fall Winter 2026.png', 'bg': '#6594c0', 'label': '2026'},
        ],
    }
    cards = coleccion_data.get(coleccion, [])
    context = {
        'coleccion': coleccion,
        'cards': cards,
    }
    return render(request, "colecciones/anio_coleccion.html", context)




# API endpoint de prueba para lista_coleccion, devuelve datos simulados JSON
@api_view(['GET'])
def lista_coleccion(request):
    nombre = request.GET.get('nombre')
    # Simulación básica
    data = [
        {'producto': 'Vestido largo', 'coleccion': nombre},
        {'producto': 'Chaqueta de cuero', 'coleccion': nombre},
    ]
    return Response(data)



