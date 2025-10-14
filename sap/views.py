
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


def execute_hana_insert(query, params=None, schema='SBOJOZF'):
    """Función auxiliar para ejecutar consultas INSERT de forma segura."""
    conn = None
    cursor = None
    try:
        conn = get_hana_connection(schema)
        if not conn:
            return False, "Error de conexión a la base de datos."

        cursor = conn.cursor()
        cursor.execute(query, params or ())

        # Para INSERT, verificamos si se afectaron filas
        if cursor.rowcount > 0:
            conn.commit()
            return True, None
        else:
            return False, "No se pudo insertar el registro"

    except Exception as e:
        logger.error(f"Error ejecutando el INSERT en HANA: {e}", exc_info=True)
        return False, str(e)
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
        query = 'SELECT "prenda_id", "tipo_prenda_nombre" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_PRENDA"'
        logger.info(f"Executing query: {query} in schema CONSUMO_TEXTIL")
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener prendas: {error}")
            return Response({"detail": f"Error al obtener prendas: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Data obtained: {data}")
        return Response(data, status=status.HTTP_200_OK)


class CantidadTelasAPIView(APIView):
    def get(self, request):
        logger.info("[CantidadTelasAPIView] GET para obtener cantidades de telas")
        query = 'SELECT "cantidad_telas_id", "cantidad_telas_numero" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_CANTIDAD_TELAS"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener cantidades de telas: {error}")
            return Response({"detail": f"Error al obtener cantidades de telas: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class UsoTelaAPIView(APIView):
    def get(self, request):
        logger.info("[UsoTelaAPIView] GET para obtener usos de tela")
        query = 'SELECT "uso_tela_id", "uso_tela_nombre" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_USO_TELA"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener usos de tela: {error}")
            return Response({"detail": f"Error al obtener usos de tela: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class BaseTextilAPIView(APIView):
    def get(self, request):
        logger.info("[BaseTextilAPIView] GET para obtener bases textiles")
        query = 'SELECT "base_textil_id", "base_textil_nombre" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_BASE_TEXTIL"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener bases textiles: {error}")
            return Response({"detail": f"Error al obtener bases textiles: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class CaracteristicaColorAPIView(APIView):
    def get(self, request):
        logger.info("[CaracteristicaColorAPIView] GET para obtener características de color")
        query = 'SELECT "caracteristica_color_id", "caracteristica_nombre" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_CARACTERISTICA_COLOR"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener características de color: {error}")
            return Response({"detail": f"Error al obtener características de color: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class AnchoUtilAPIView(APIView):
    def get(self, request):
        logger.info("[AnchoUtilAPIView] GET para obtener anchos útiles")
        query = 'SELECT "ancho_util_id", "ancho_util_metros" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_ANCHO_UTIL"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener anchos útiles: {error}")
            return Response({"detail": f"Error al obtener anchos útiles: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class PropiedadesTelaAPIView(APIView):
    def get(self, request):
        logger.info("[PropiedadesTelaAPIView] GET para obtener propiedades de tela")
        query = 'SELECT "propiedades_tela_id", \'Propiedad \' || "propiedades_tela_id" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_PROPIEDADES_TELA"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener propiedades de tela: {error}")
            return Response({"detail": f"Error al obtener propiedades de tela: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class VarianteAPIView(APIView):
    def get(self, request):
        logger.info("[VarianteAPIView] GET para obtener variantes")
        query = 'SELECT "variante_id", \'Variante \' || "numero_variante" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_VARIANTE"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener variantes: {error}")
            return Response({"detail": f"Error al obtener variantes: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class DescripcionAPIView(APIView):
    def get(self, request):
        logger.info("[DescripcionAPIView] GET para obtener descripciones")
        query = 'SELECT "descripcion_id", "detalle_descripcion" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_DESCRIPCION"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener descripciones: {error}")
            return Response({"detail": f"Error al obtener descripciones: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)


class TerminacionAPIView(APIView):
    def get(self, request):
        logger.info("[TerminacionAPIView] GET para obtener terminaciones")
        query = 'SELECT "terminacion_id", "categoria_terminacion" || \' - \' || "tipo_terminacion" as "nombre" FROM "CONSUMO_TEXTIL"."DIM_TERMINACION"'
        data, error = execute_hana_query(query, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener terminaciones: {error}")
            return Response({"detail": f"Error al obtener terminaciones: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        
        print(f"Image URL: {image.image.url}")

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
    Vista para obtener datos de consumo textil filtrados desde VIEW_FACT_CONSUMO.
    """
    def get(self, request):
        logger.info("[ConsumoTextilAPIView] Solicitud GET para obtener consumo textil")
        logger.info(f"[ConsumoTextilAPIView] Query params: {dict(request.query_params)}")
        logger.info(f"[ConsumoTextilAPIView] Query params type: {type(request.query_params)}")

        # Obtener parámetros de filtro
        tipo_prenda = request.query_params.get('tipo_prenda')
        cantidad_telas = request.query_params.get('cantidad_telas')
        numero_variante = request.query_params.get('numero_variante')
        uso_tela = request.query_params.get('uso_tela')
        base_textil = request.query_params.get('base_textil')
        caracteristica_color = request.query_params.get('caracteristica_color')
        ancho_util = request.query_params.get('ancho_util')

        logger.info(f"[ConsumoTextilAPIView] tipo_prenda: '{tipo_prenda}' (type: {type(tipo_prenda)})")
        logger.info(f"[ConsumoTextilAPIView] cantidad_telas: '{cantidad_telas}' (type: {type(cantidad_telas)})")
        logger.info(f"[ConsumoTextilAPIView] numero_variante: '{numero_variante}' (type: {type(numero_variante)})")

        # --- Lógica de Decisión Refactorizada ---

        # Caso 1: No se proporciona `tipo_prenda`. Devolver la lista de todas las prendas únicas.
        if not tipo_prenda:
            logger.info("[ConsumoTextilAPIView] Caso 1: Devolviendo lista de prendas.")
            query = 'SELECT DISTINCT "tipo_prenda_nombre" FROM "CONSUMO_TEXTIL"."VIEW_FACT_CONSUMO"'
            params = []
        
        # Caso 2: Se proporciona `tipo_prenda`, `cantidad_telas` y `numero_variante`. Devolver el detalle del consumo.
        elif tipo_prenda and cantidad_telas and numero_variante:
            logger.info(f"[ConsumoTextilAPIView] Caso 2: Devolviendo detalle de consumo para {tipo_prenda}, {cantidad_telas} telas, variante {numero_variante}.")
            query = '''
                SELECT "uso_tela", "base_textil", "caracteristica_color", "consumo_mtr", "ancho_util_metros", "tipo_terminacion"
                FROM "CONSUMO_TEXTIL"."VIEW_FACT_CONSUMO"
                WHERE "tipo_prenda" = ?
                  AND "cantidad_telas" = ?
                  AND "numero_variante" = ?
            '''
            params = [tipo_prenda, cantidad_telas, numero_variante]

            # Agregar filtros adicionales condicionalmente
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

            query += ' ORDER BY "consumo_id"'
        
        # Caso 3: Se proporciona solo `tipo_prenda`. Devolver las variantes disponibles para esa prenda.
        elif tipo_prenda:
            logger.info(f"[ConsumoTextilAPIView] Caso 3: Devolviendo variantes para {tipo_prenda}.")
            query = '''
                SELECT DISTINCT "cantidad_telas", "numero_variante", "descripcion_variante", "tipo_terminacion"
                FROM "CONSUMO_TEXTIL"."VIEW_FACT_CONSUMO"
                WHERE "tipo_prenda" = ?
                ORDER BY "cantidad_telas", "numero_variante" ASC
            '''
            params = [tipo_prenda]

        else:
            # Caso no manejado, devolver error.
            logger.warning(f"[ConsumoTextilAPIView] Combinación de parámetros no manejada: {dict(request.query_params)}")
            return Response({"error": "Combinación de parámetros inválida."}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Executing query: {query} with params: {params}")

        data, error = execute_hana_query(query, params=params, schema='CONSUMO_TEXTIL')

        if error:
            logger.error(f"Error al obtener consumo textil: {error}")
            return Response({"detail": f"Error al obtener consumo textil: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Datos obtenidos: {len(data)} registros")
        return Response(data, status=status.HTTP_200_OK)


class FactConsumoAPIView(APIView):
    """
    Vista para crear nuevos registros en FACT_CONSUMO.
    """
    def post(self, request):
        logger.info("[FactConsumoAPIView] Solicitud POST para crear nuevo registro en FACT_CONSUMO")
        data = request.data

        # Validar campos requeridos
        required_fields = [
            'prenda_id', 'cantidad_telas_id', 'uso_tela_id', 'base_textil_id',
            'caracteristica_color_id', 'ancho_util_id', 'propiedades_tela_id', 'consumo_mtr'
        ]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"error": f"El campo {field} es requerido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validar que consumo_mtr sea un número positivo
        try:
            consumo_mtr = float(data.get('consumo_mtr', 0))
            if consumo_mtr <= 0:
                return Response(
                    {"error": "El consumo_mtr debe ser un número positivo"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "El consumo_mtr debe ser un número válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construir la consulta INSERT
        query = '''
            INSERT INTO "CONSUMO_TEXTIL"."FACT_CONSUMO"
            ("prenda_id", "cantidad_telas_id", "uso_tela_id", "base_textil_id",
             "caracteristica_color_id", "ancho_util_id", "propiedades_tela_id",
             "consumo_mtr", "variante_id", "descripcion_id", "terminacion_id")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        params = [
            data.get('prenda_id'),
            data.get('cantidad_telas_id'),
            data.get('uso_tela_id'),
            data.get('base_textil_id'),
            data.get('caracteristica_color_id'),
            data.get('ancho_util_id'),
            data.get('propiedades_tela_id'),
            consumo_mtr,
            data.get('variante_id') if data.get('variante_id') else None,
            data.get('descripcion_id') if data.get('descripcion_id') else None,
            data.get('terminacion_id') if data.get('terminacion_id') else None,
        ]

        logger.info(f"Executing INSERT query with params: {params}")

        # Para INSERT, necesitamos una función especial que no espere un result set
        success, error = execute_hana_insert(query, params=params, schema='CONSUMO_TEXTIL')

        if not success:
            logger.error(f"Error al insertar registro en FACT_CONSUMO: {error}")
            return Response(
                {"error": f"Error al crear el referente: {error}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info("Registro creado exitosamente en FACT_CONSUMO")
        return Response(
            {"success": "Referente creado exitosamente"},
            status=status.HTTP_201_CREATED
        )

# ... (Otras vistas y lógica heredada se mantienen aquí para no romper la funcionalidad existente)
