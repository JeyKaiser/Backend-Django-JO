
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .HANA.conf import get_hana_connection
from .HANA import queries as hana_queries # Mantener para la lógica existente
from .services import parametros as parametros_service # Importar el nuevo servicio

logger = logging.getLogger(__name__)

# --- Vistas para Tablas Maestras (GET) ---

class GenericTableView(APIView):
    """
    Una vista genérica para obtener todos los registros de una tabla maestra.
    El nombre de la tabla se pasa desde urls.py.
    """
    def get(self, request, table_name):
        logger.info(f"[GenericTableView] Solicitud GET para la tabla: {table_name}")
        data, error = parametros_service.get_all_from_table(table_name)
        
        if error:
            # Si la tabla no es válida o hay un error de BD
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data, status=status.HTTP_200_OK)


# --- Vista para el recurso de Parámetros (GET y POST) ---

class ParametrosAPIView(APIView):
    """
    Maneja las operaciones GET para listar y POST para crear parámetros.
    """
    def get(self, request):
        """
        Obtiene todos los parámetros existentes.
        """
        logger.info("[ParametrosAPIView] Solicitud GET para listar parámetros")
        # Reutilizamos la lógica anterior para mantener la compatibilidad
        query = hana_queries.query_get_parametros()
        
        # La función execute_hana_query original está en este archivo, la adaptamos
        # para usar el nuevo esquema.
        data, error = execute_hana_query(query, schema=parametros_service.SCHEMA_NAME)

        if error:
            return Response({"detail": f"Error al obtener parámetros: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crea un nuevo parámetro a partir de los datos del body.
        """
        logger.info("[ParametrosAPIView] Solicitud POST para crear un nuevo parámetro")
        data = request.data
        
        success, message = parametros_service.create_parametro(data)
        
        if not success:
            # Error de validación o de base de datos
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Éxito
        return Response({"success": message}, status=status.HTTP_201_CREATED)


# --- Lógica y Vistas Heredadas (para mantener compatibilidad) ---
# (Se mantiene la lógica anterior que no se relaciona con los nuevos endpoints)

def execute_hana_query(query, params=None, schema='SBOJOZF'):
    """Función auxiliar para ejecutar consultas de forma segura."""
    conn = None
    cursor = None
    try:
        conn = get_hana_connection(schema)
        if not conn:
            return None, "Error de conexión a la base de datos."
        
        cursor = conn.cursor()
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

class CollectionsAPIView(APIView):
    def get(self, request):
        logger.info("[CollectionsAPIView] GET para obtener colecciones")
        query = hana_queries.queryGetCollections()
        data, error = execute_hana_query(query)

        if error:
            return Response({"detail": f"Error al obtener colecciones: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data, status=status.HTTP_200_OK)

# ... (Otras vistas y lógica heredada se mantienen aquí para no romper la funcionalidad existente)
