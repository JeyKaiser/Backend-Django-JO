
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .HANA.conf import get_hana_connection
from .HANA import queries as hana_queries # Mantener para la lógica existente
from .services import parametros as parametros_service # Importar el nuevo servicio
from .models import Image
from django.http import Http404

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

class ParametrosViewAPIView(APIView):
    def get(self, request):
        logger.info("[ParametrosViewAPIView] GET para obtener parametros view")
        query = hana_queries.query_get_parametros_view()
        data, error = execute_hana_query(query, schema='GARMENT_PRODUCTION_CONTROL')

        if error:
            return Response({"detail": f"Error al obtener parametros view: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data, status=status.HTTP_200_OK)

class PrendasAPIView(APIView):
    def get(self, request):
        logger.info("[PrendasAPIView] GET para obtener prendas")
        query = 'SELECT * FROM "DIM_PRENDA"'
        logger.info(f"Executing query: {query} in schema CONSUMO_TEXTIL")
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener prendas: {error}")
            return Response({"detail": f"Error al obtener prendas: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.info(f"Data obtained: {data}")
        return Response(data, status=status.HTTP_200_OK)


# --- Vistas para Servidor de Imágenes ---

class ImageUploadView(APIView):
    """
    Vista para subir imágenes.
    """
    def post(self, request):
        logger.info("[ImageUploadView] Solicitud POST para subir imagen")
        title = request.data.get('title', '')
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({"error": "No se proporcionó ninguna imagen"}, status=status.HTTP_400_BAD_REQUEST)

        image = Image.objects.create(title=title, image=image_file)
        return Response({
            "id": image.id,
            "title": image.title,
            "image_url": image.image.url,
            "uploaded_at": image.uploaded_at
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Vista para obtener imágenes filtradas por título.
        """
        logger.info("[ImageUploadView] Solicitud GET para obtener imágenes filtradas")
        title_filter = request.query_params.get('title', '')

        if title_filter:
            images = Image.objects.filter(title__icontains=title_filter).order_by('-uploaded_at')
        else:
            images = Image.objects.all().order_by('-uploaded_at')

        data = [{
            "id": img.id,
            "title": img.title,
            "image_url": img.image.url,
            "uploaded_at": img.uploaded_at
        } for img in images]
        return Response(data, status=status.HTTP_200_OK)


class ImageServeView(APIView):
    """
    Vista para obtener una imagen por ID.
    """
    def get(self, request, image_id):
        logger.info(f"[ImageServeView] Solicitud GET para imagen ID: {image_id}")
        try:
            image = Image.objects.get(id=image_id)
            return Response({
                "id": image.id,
                "title": image.title,
                "image_url": image.image.url,
                "uploaded_at": image.uploaded_at
            }, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            raise Http404("Imagen no encontrada")


class ImageListView(APIView):
    """
    Vista para listar todas las imágenes.
    """
    def get(self, request):
        logger.info("[ImageListView] Solicitud GET para listar imágenes")
        images = Image.objects.all().order_by('-uploaded_at')
        data = [{
            "id": img.id,
            "title": img.title,
            "image_url": img.image.url,
            "uploaded_at": img.uploaded_at
        } for img in images]
        return Response(data, status=status.HTTP_200_OK)


class ConsumoTextilAPIView(APIView):
    """
    Vista para obtener datos de consumo textil filtrados desde V_FACT_CONSUMO_LEGIBLE.
    """
    def get(self, request):
        logger.info("[ConsumoTextilAPIView] Solicitud GET para obtener consumo textil")

        # Obtener parámetros de filtro
        tipo_prenda = request.query_params.get('tipo_prenda')
        cantidad_telas = request.query_params.get('cantidad_telas')
        uso_tela = request.query_params.get('uso_tela')
        base_textil = request.query_params.get('base_textil')
        caracteristica_color = request.query_params.get('caracteristica_color')
        ancho_util = request.query_params.get('ancho_util')

        # Si no hay tipo_prenda, devolver las cantidades de telas individuales por prenda
        if not tipo_prenda:
            query = '''
                SELECT
                    "tipo_prenda",
                    "cantidad_telas" as "conteo_telas_unicas"
                FROM "CONSUMO_TEXTIL"."V_FACT_CONSUMO_LEGIBLE"
                GROUP BY "tipo_prenda", "cantidad_telas"
                ORDER BY "tipo_prenda", "cantidad_telas"
            '''

            logger.info(f"Executing count query: {query}")

            data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

            if error:
                logger.error(f"Error al obtener conteo de telas: {error}")
                return Response({"detail": f"Error al obtener conteo de telas: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Conteo de telas obtenido: {len(data)} registros")
            return Response(data, status=status.HTTP_200_OK)

        # Si hay tipo_prenda pero no cantidad_telas, devolver solo los conteos para ese tipo específico
        if tipo_prenda and not cantidad_telas:
            query = '''
                SELECT DISTINCT
                    "cantidad_telas" as "conteo_telas_unicas"
                FROM "CONSUMO_TEXTIL"."V_FACT_CONSUMO_LEGIBLE"
                WHERE "tipo_prenda" = ?
                ORDER BY "cantidad_telas"
            '''

            logger.info(f"Executing filtered count query for tipo_prenda: {tipo_prenda}")

            data, error = execute_hana_query(query, params=[tipo_prenda], schema='CONSUMO_TEXTIL')

            if error:
                logger.error(f"Error al obtener conteo de telas filtrado: {error}")
                return Response({"detail": f"Error al obtener conteo de telas filtrado: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Conteo de telas filtrado obtenido: {len(data)} registros para {tipo_prenda}")
            return Response(data, status=status.HTTP_200_OK)

        # Si hay tipo_prenda, devolver datos filtrados con consulta específica
        query = '''
            SELECT
                "uso_tela" AS "uso_en_prenda",
                "base_textil" AS "base_textil",
                "caracteristica_color" AS "color",
                "ancho_util_metros" AS "ancho_tela",
                "propiedades_tela" AS "propiedades",
                "consumo_mtr" AS "consumo"
            FROM "CONSUMO_TEXTIL"."V_FACT_CONSUMO_LEGIBLE"
            WHERE "tipo_prenda" = ?
        '''

        params = [tipo_prenda]

        # Agregar filtros adicionales condicionalmente
        if cantidad_telas:
            query += ' AND "cantidad_telas" = ?'
            params.append(int(cantidad_telas))

        if uso_tela:
            query += ' AND "uso_tela" = ?'
            params.append(uso_tela)

        if base_textil:
            query += ' AND "base_textil" = ?'
            params.append(base_textil)

        if caracteristica_color:
            query += ' AND "caracteristica_color" = ?'
            params.append(caracteristica_color)

        if ancho_util:
            query += ' AND "ancho_util_metros" = ?'
            params.append(float(ancho_util))

        query += ' ORDER BY "uso_tela"'

        logger.info(f"Executing query: {query} with params: {params}")

        data, error = execute_hana_query(query, params=params, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener consumo textil: {error}")
            return Response({"detail": f"Error al obtener consumo textil: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Datos obtenidos: {len(data)} registros")
        return Response(data, status=status.HTTP_200_OK)

# ... (Otras vistas y lógica heredada se mantienen aquí para no romper la funcionalidad existente)
