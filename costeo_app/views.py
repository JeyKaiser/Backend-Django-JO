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
        print("Django [ColeccionesAPIView]: Solicitud GET recibida para obtener todas las colecciones desde Supabase")

        # Simulación de datos de colecciones (reemplaza con lógica real de Supabase)
        colecciones = [
            {
                'id': '2024',
                'label': 'Winter Sun 2024',
                'img': '/img/1.WINTER_SUN/Winter Sun 2024.png',
                'bg': '#feea4d',
                'status': 'active',
                'season': 'Winter Sun',
                'year': '2024',
                'lastUpdated': 'N/A'
            },
            {
                'id': '2025',
                'label': 'Resort RTW 2025',
                'img': '/img/2.RESORT_RTW/Resort RTW 2025.png',
                'bg': '#70a7ff',
                'status': 'active',
                'season': 'Resort RTW',
                'year': '2025',
                'lastUpdated': 'N/A'
            }
        ]

        print(f"Django [ColeccionesAPIView]: Enviando {len(colecciones)} colecciones desde Supabase")
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

        # Simulación de creación exitosa (reemplaza con lógica real de Supabase)
        return Response(
            {"message": "Collection created successfully"},
            status=status.HTTP_201_CREATED
        )

class TrazabilidadAPIView(APIView):
    def get(self, request, id_referencia):
        logger.info(f"Django [TrazabilidadAPIView]: Solicitud GET recibida para la trazabilidad de la referencia con ID: {id_referencia}")

        # Simulación de datos de trazabilidad (reemplaza con lógica real de Supabase)
        data_from_db = [
            {
                'ID_FASE': 1,
                'NOMBRE_FASE': 'JO',
                'FECHA_INICIO': '2024-01-01',
                'FECHA_FIN': '2024-01-15'
            },
            {
                'ID_FASE': 2,
                'NOMBRE_FASE': 'MD Creación Ficha',
                'FECHA_INICIO': '2024-01-16',
                'FECHA_FIN': None
            }
        ]

        return Response(data_from_db, status=status.HTTP_200_OK)

    def post(self, request, id_referencia):
        data = request.data
        id_fase = data.get('ID_FASE')

        # Simulación de actualización exitosa (reemplaza con lógica real de Supabase)
        return Response({'message': 'Traceability record created successfully'}, status=status.HTTP_201_CREATED)

class TrazabilidadCurrentAPIView(APIView):
    def get(self, request, id_referencia):
        logger.info(f"Django [TrazabilidadCurrentAPIView]: Solicitud GET recibida para la fase actual de la referencia con ID: {id_referencia}")

        # Simulación de fase actual (reemplaza con lógica real de Supabase)
        current_phase = {
            'ID_FASE': 2,
            'NOMBRE_FASE': 'MD Creación Ficha',
            'FECHA_INICIO': '2024-01-16',
            'ESTADO': 'En Progreso'
        }

        return Response(current_phase, status=status.HTTP_200_OK)

class FasesAPIView(APIView):
    def get(self, request, codigo_fase=None):
        if codigo_fase:
            logger.info(f"Django [FasesAPIView]: Solicitud GET recibida para la fase con código: {codigo_fase}")

            # Simulación de búsqueda por código (reemplaza con lógica real de Supabase)
            phases = {
                'JO': {'codigo': 'JO', 'nombre': 'JO', 'descripcion': 'Fase inicial'},
                'MD001': {'codigo': 'MD001', 'nombre': 'MD Creación Ficha', 'descripcion': 'Creación de ficha técnica'}
            }

            phase_data = phases.get(codigo_fase)
            if not phase_data:
                return Response({'detail': 'Phase not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(phase_data, status=status.HTTP_200_OK)
        else:
            logger.info(f"Django [FasesAPIView]: Solicitud GET recibida para obtener todas las fases")

            # Simulación de todas las fases (reemplaza con lógica real de Supabase)
            all_phases = [
                {'codigo': 'JO', 'nombre': 'JO', 'descripcion': 'Fase inicial'},
                {'codigo': 'MD001', 'nombre': 'MD Creación Ficha', 'descripcion': 'Creación de ficha técnica'},
                {'codigo': 'MD002', 'nombre': 'MD Creativo', 'descripcion': 'Fase creativa'},
                {'codigo': 'PT001', 'nombre': 'PT Técnico', 'descripcion': 'Fase técnica de producción'}
            ]

            return Response(all_phases, status=status.HTTP_200_OK)

class ReferenciaAPIView(APIView):
    def post(self, request):
        data = request.data

        codigo_referencia = data.get('CODIGO_REFERENCIA')
        id_coleccion = data.get('ID_COLECCION')
        nombre_referencia = data.get('NOMBRE_REFERENCIA')

        # Simulación de creación exitosa (reemplaza con lógica real de Supabase)
        return Response({'message': 'Reference created successfully'}, status=status.HTTP_201_CREATED)

class ReferenciaDetalleAPIView(APIView):
    def get(self, request, codigo_referencia):
        logger.info(f"Django [ReferenciaDetalleAPIView]: Solicitud GET recibida para codigo_referencia: {codigo_referencia}")

        # Simulación de detalle de referencia (reemplaza con lógica real de Supabase)
        reference_detail = {
            'codigo_referencia': codigo_referencia,
            'nombre': f'Referencia {codigo_referencia}',
            'coleccion': 'Winter Sun 2024',
            'estado': 'Activo'
        }

        return Response(reference_detail, status=status.HTTP_200_OK)

class ReferenciaSearchAPIView(APIView):
    def get(self, request):
        search_term = request.query_params.get('search', '')

        # Simulación de búsqueda (reemplaza con lógica real de Supabase)
        search_results = [
            {
                'codigo': 'REF001',
                'nombre': f'Resultado para "{search_term}"',
                'coleccion': 'Winter Sun 2024'
            }
        ]

        return Response(search_results, status=status.HTTP_200_OK)

class AnioColeccionAPIView(APIView):
    def get(self, request, coleccion): # 'coleccion' can be either slug or numeric ID
        print(f"Django [AnioColeccionAPIView]: Coleccion ID/slug recibido: '{coleccion}'")
        
        # Mapping from numeric IDs to slugs and vice versa
        id_to_slug = {
            '063': 'winter-sun', '085': 'winter-sun', '105': 'winter-sun',
            '065': 'resort-rtw', '084': 'resort-rtw', '106': 'resort-rtw',
            '067': 'spring-summer', '088': 'spring-summer', '110': 'spring-summer',
            '070': 'summer-vacation', '094': 'summer-vacation',
            '071': 'pre-fall', '096': 'pre-fall',
            '075': 'fall-winter', '102': 'fall-winter',
        }
        
        slug_to_name = {
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
        
        # Determine if input is numeric ID or slug, then get the appropriate slug
        if coleccion.isdigit() or coleccion in id_to_slug:
            # Input is a numeric ID, convert to slug
            slug = id_to_slug.get(coleccion)
            if not slug:
                print(f"Django [AnioColeccionAPIView]: ERROR: Numeric ID '{coleccion}' no encontrado.")
                return Response({'detail': f'Collection ID "{coleccion}" not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Input is already a slug
            slug = coleccion
            
        # Get data using the slug
        cards = coleccion_data.get(slug, [])
        collection_name = slug_to_name.get(slug, slug)

        if cards:
            print(f"Django [AnioColeccionAPIView]: Colección '{slug}' encontrada. Enviando {len(cards)} tarjetas.")
            return Response({
                'nombre_coleccion': collection_name,
                'anios': cards
            }, status=status.HTTP_200_OK)
        else:
            print(f"Django [AnioColeccionAPIView]: ERROR: Colección '{coleccion}' NO encontrada.")
            return Response({'detail': f'Collection "{coleccion}" not found'}, status=status.HTTP_404_NOT_FOUND)
        


class ReferenciasAnioAPIView(APIView):
    def get(self, request, collection_id):
        logger.info(f"Django [ReferenciasAPIView]: Solicitud GET recibida para collection_id: {collection_id}")

        # Simulación de referencias por colección (reemplaza con lógica real de Supabase)
        references = [
            {
                'codigo': 'REF001',
                'nombre': 'Bikini Top - Tirantes',
                'estado': 'Activo'
            },
            {
                'codigo': 'REF002',
                'nombre': 'Bikini Bottom - Alto',
                'estado': 'En Desarrollo'
            }
        ]

        logger.info(f"Devolviendo {len(references)} referencias para la colección {collection_id}")
        return Response(references, status=status.HTTP_200_OK)







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

                # Simulación de datos de telas e insumos (reemplaza con lógica real de Supabase)
                telas_data = [
                    {
                        'codigo': 'TELA001',
                        'nombre': 'Lycra Vita',
                        'color': 'Azul',
                        'consumo': 0.17
                    }
                ]
                insumos_data = [
                    {
                        'codigo': 'INS001',
                        'nombre': 'Hilo de coser',
                        'cantidad': 10
                    }
                ]

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
       


# apps/costeo_app/views.py (Fragmento relevante)

# ...
class FaseDetalleAPIView(APIView):
    def get(self, request, collection_id, referencia_id, fasesSlug):
        # ...
        if fasesSlug == 'md-creacion-ficha':
            # FUNCIONES REMOVIDAS:
            # telas_data = telasPorReferencia(referencia_id, collection_id)
            # insumos_data = insumosPorReferencia(referencia_id, collection_id)
            # TODO: Implementar nueva lógica para obtener telas e insumos
            telas_data = []
            insumos_data = []

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
            # Simulación de búsqueda PT Code (reemplaza con lógica real de Supabase)
            search_result = {
                'pt_code': pt_code,
                'collection': 'Winter Sun 2024',
                'referencia': 'REF001'
            }

            return Response(search_result, status=status.HTTP_200_OK)
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


# =====================================================================================
# VISTAS DE API PARA LA BASE DE DATOS DIMENSIONAL 'CONSUMO_TEXTIL'
# =====================================================================================

class DimPrendaList(generics.ListAPIView):
    queryset = DimPrenda.objects.all()
    serializer_class = DimPrendaSerializer

class DimCantidadTelasList(generics.ListAPIView):
    queryset = DimCantidadTelas.objects.all()
    serializer_class = DimCantidadTelasSerializer

class DimUsoTelaList(generics.ListAPIView):
    queryset = DimUsoTela.objects.all()
    serializer_class = DimUsoTelaSerializer

class DimBaseTextilList(generics.ListAPIView):
    queryset = DimBaseTextil.objects.all()
    serializer_class = DimBaseTextilSerializer

class DimCaracteristicaColorList(generics.ListAPIView):
    queryset = DimCaracteristicaColor.objects.all()
    serializer_class = DimCaracteristicaColorSerializer

class DimAnchoUtilList(generics.ListAPIView):
    queryset = DimAnchoUtil.objects.all()
    serializer_class = DimAnchoUtilSerializer

class DimPropiedadesTelaList(generics.ListAPIView):
    queryset = DimPropiedadesTela.objects.all()
    serializer_class = DimPropiedadesTelaSerializer

class DimVarianteList(generics.ListAPIView):
    queryset = DimVariante.objects.all()
    serializer_class = DimVarianteSerializer

class DimDescripcionList(generics.ListAPIView):
    queryset = DimDescripcion.objects.all()
    serializer_class = DimDescripcionSerializer

class DimTerminacionList(generics.ListAPIView):
    queryset = DimTerminacion.objects.all()
    serializer_class = DimTerminacionSerializer

class FactConsumoCreate(APIView):
    def post(self, request, format=None):
        serializer = FactConsumoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
