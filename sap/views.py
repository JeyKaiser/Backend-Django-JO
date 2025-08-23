from .HANA.conf import get_hana_connection
from .HANA import queries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

STANDARD_FASES_DISPONIBLES = [
    {"slug": "jo", "nombre": "JO"},
    {"slug": "md-creacion-ficha", "nombre": "MD CREACION FICHA"},
    {"slug": "md-creativo", "nombre": "MD CREATIVO"},
    {"slug": "md-corte", "nombre": "MD CORTE"},
    {"slug": "md-confeccion", "nombre": "MD CONFECCION"},
    {"slug": "md-fitting", "nombre": "MD FITTING"},
    {"slug": "md-tecnico", "nombre": "MD TECNICO"},
    {"slug": "md-trazador", "nombre": "MD TRAZADOR"},
    {"slug": "costeo", "nombre": "COSTEO"},
    {"slug": "pt-tecnico", "nombre": "PT TECNICO"},
    {"slug": "pt-cortador", "nombre": "PT CORTADOR"},
    {"slug": "pt-fitting", "nombre": "PT FITTING"},
    {"slug": "pt-trazador", "nombre": "PT TRAZADOR"},
]

def execute_hana_query(query, params=None, schema='SBOJOZF'):
    """Función auxiliar para ejecutar consultas de forma segura."""
    conn = None
    cursor = None
    try:
        conn = get_hana_connection(schema)
        if not conn:
            # La conexión falló, get_hana_connection ya registró el error.
            return None, "Error de conexión a la base de datos."
        
        cursor = conn.cursor()
        
        # SET SCHEMA ya no es necesario aquí porque se establece en la conexión.
        # cursor.execute(queries.querySelectDataBase().format(schema))
        
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        
        if not rows:
            return [], None

        column_names = [desc[0] for desc in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        return data, None
    except Exception as e:
        logger.error(f"Error ejecutando la consulta en HANA: {e}", exc_info=True)
        return None, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info(f"Conexión a HANA para el esquema {schema} cerrada.")

def referenciasPorAnio(collection_id):
    logger.info(f"Iniciando consulta a SAP para collection_id {collection_id}")
    query = queries.queryReferenciasPorAnio()
    data, error = execute_hana_query(query, (collection_id,))
    
    if error:
        # El error ya fue loggeado en la función auxiliar
        return [] # Devolver una lista vacía en caso de error

    for item in data:
        picture = item.get("U_GSP_Picture")
        if picture:
            item["U_GSP_Picture"] = f"https://johannaortiz.net/media/ImagesJOServer/{picture.replace('\\', '/')}"
    
    logger.info(f"Datos procesados a devolver: {len(data)} registros.")
    return data

def telasPorReferencia(referencia_id, collection_id):
    logger.info(f"Buscando telas para referencia: {referencia_id}, Colección: {collection_id}")
    query = queries.queryTelasPorReferencia()
    data, error = execute_hana_query(query, (referencia_id, collection_id))
    return data if not error else []

def insumosPorReferencia(referencia_id, collection_id):
    logger.info(f"Buscando insumos para referencia: {referencia_id}, Colección: {collection_id}")
    query = queries.queryInsumosPorReferencia()
    data, error = execute_hana_query(query, (referencia_id, collection_id))
    return data if not error else []

def consumosPorReferencia(pt_code):
    logger.info(f"Iniciando búsqueda de consumos para referencia: {pt_code}")
    query = queries.queryConsumosPorReferencia()
    data, error = execute_hana_query(query, (pt_code,))
    return data if not error else []

# --- API Views Refactorizadas ---

class TelasAPIView(APIView):
    def get(self, request, referencia_id):
        logger.info(f"[TelasAPIView] GET para referencia_id: {referencia_id}")
        collection_id = request.query_params.get('collectionId')
        if not collection_id:
            return Response({"detail": "El parámetro 'collectionId' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = telasPorReferencia(referencia_id, collection_id)
        return Response(data, status=status.HTTP_200_OK)

class CollectionsAPIView(APIView):
    def get(self, request):
        logger.info("[CollectionsAPIView] GET para obtener colecciones")
        query = queries.queryGetCollections()
        data, error = execute_hana_query(query)

        if error:
            return Response({"detail": f"Error al obtener colecciones: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        collections_list = [
            {'U_GSP_SEASON': item.get('U_GSP_SEASON'), 'Name': item.get('Name')}
            for item in data
        ]
        return Response(collections_list, status=status.HTTP_200_OK)

class ConsumosAPIView(APIView):
    def get(self, request):
        reference_code = request.query_params.get('reference', '').strip()
        logger.info(f"[ConsumosAPIView] GET para referencia: {reference_code}")

        if not reference_code:
            return Response({"success": False, "error": "El parámetro 'reference' es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        if not reference_code.upper().startswith('PT'):
            return Response({"success": False, "error": "Formato de referencia inválido"}, status=status.HTTP_400_BAD_REQUEST)

        data = consumosPorReferencia(reference_code)
        
        response_data = {
            "success": True,
            "data": data,
            "count": len(data),
            "referenceCode": reference_code
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Las vistas y funciones que no interactúan con la base de datos HANA no necesitan cambios,
# como getModeloDetalle.

def getModeloDetalle(request, referencia_id):
    logger.info(f"Obteniendo detalle completo del modelo para referencia: {referencia_id}")
    combined_data = {    
        'nombre': f"Referencia {referencia_id}",   
        'fases_disponibles': STANDARD_FASES_DISPONIBLES 
    }
    logger.info(f"Datos combinados del modelo para {referencia_id}: {combined_data}")
    return combined_data

def searchPTCode(pt_code):
    logger.info(f"Buscando PT Code: {pt_code}")
    query = queries.querySearchPTCode()
    data, error = execute_hana_query(query, (pt_code,))
    return data if not error else []

def models(referencia_id):
    logger.info(f"Buscando modelos para referencia: {referencia_id}")
    query = queries.queryModelsPorReferencia()
    data, error = execute_hana_query(query, (referencia_id,))
    return data if not error else []
