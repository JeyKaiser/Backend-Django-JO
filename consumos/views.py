import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sap.views import execute_hana_query

logger = logging.getLogger(__name__)

class ConsumosAPIView(APIView):
    """
    API migrada desde Frontend para gestionar consultas de consumos de telas
    """
    def get(self, request):
        """
        Obtener consumos de telas por referencia
        """
        try:
            reference = request.GET.get('reference')
            
            if not reference:
                return Response({
                    'success': False,
                    'error': 'El parámetro reference es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            logger.info(f"[ConsumosAPIView] Consultando consumos para referencia: {reference}")
            
            # Consulta de consumos de telas por referencia - Corregida y probada en DBeaver
            sql = """
                SELECT 
                    T3."Name" AS "COLECCION",
                    T1."U_GSP_Desc" AS "NOMBRE_REF",
                    T2."U_GSP_SchLinName" AS "USO_EN_PRENDA",
                    T2."U_GSP_ItemCode" AS "COD_TELA",
                    T2."U_GSP_ItemName" AS "NOMBRE_TELA",
                    T2."U_GSP_QuantMsr" AS "CONSUMO"
                FROM "@GSP_TCMODEL" T1
                INNER JOIN "@GSP_TCMODELMAT" T2
                    ON T1."Name" = T2."U_GSP_ModelCode"
                INNER JOIN "@GSP_TCCOLLECTION" T3
                    ON T1."U_GSP_COLLECTION" = T3."U_GSP_SEASON"
                INNER JOIN "@GSP_TCMATERIAL" T4
                    ON T1."U_GSP_MATERIAL" = T4."Code"
                INNER JOIN "@GSP_TCSCHEMA" T5
                    ON T1."U_GSP_Schema" = T5."Code"
                WHERE T1."U_GSP_REFERENCE" = ? 
                AND T2."U_GSP_SchName" = 'TELAS'
                ORDER BY T2."U_GSP_SchName" DESC
            """
            
            # Ejecutar consulta con el parámetro exacto (sin wildcards) usando esquema SBOJOZF
            data, error = execute_hana_query(sql, [reference], schema='SBOJOZF')
            
            if error:
                logger.error(f"[ConsumosAPIView] Error de BD: {error}")
                return Response({
                    'success': False,
                    'error': f'Error de base de datos: {error}',
                    'referenceCode': reference
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Preparar respuesta con estructura similar al frontend original
            response_data = {
                'success': True,
                'data': data or [],
                'count': len(data or []),
                'referenceCode': reference,
                'message': f'Consumos obtenidos para la referencia {reference}' if data else f'No se encontraron consumos para la referencia {reference}'
            }
            
            logger.info(f"[ConsumosAPIView] Enviando {len(data or [])} consumos para referencia {reference}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[ConsumosAPIView] Error: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': f'Error interno del servidor: {str(e)}',
                'referenceCode': request.GET.get('reference', 'N/A')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Crear nuevo consumo de tela para una referencia
        """
        try:
            data = request.data
            logger.info(f"[ConsumosAPIView] POST crear consumo para referencia: {data.get('referencia', 'N/A')}")
            
            # Validar campos requeridos
            required_fields = ['referencia', 'codigo_tela', 'cantidad_consumo', 'unidad_medida']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return Response({
                    'success': False,
                    'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Insertar nuevo consumo
            insert_sql = """
                INSERT INTO SBOJOZF."@GSP_TCCONSUMPTION" (
                    "U_GSP_REFERENCE", "U_GSP_ITEM_CODE", "U_GSP_QUANTITY", "U_GSP_UNIT"
                ) VALUES (?, ?, ?, ?)
            """
            
            params = [
                data.get('referencia'),
                data.get('codigo_tela'),
                data.get('cantidad_consumo'),
                data.get('unidad_medida')
            ]
            
            result_data, create_error = execute_hana_query(insert_sql, params)
            
            if create_error:
                logger.error(f"[ConsumosAPIView] Error creando consumo: {create_error}")
                return Response({
                    'success': False,
                    'error': f'Error creando consumo: {create_error}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            logger.info(f"[ConsumosAPIView] Consumo creado exitosamente para referencia {data.get('referencia')}")
            return Response({
                'success': True,
                'message': 'Consumo creado exitosamente',
                'data': {
                    'referencia': data.get('referencia'),
                    'codigo_tela': data.get('codigo_tela'),
                    'cantidad_consumo': data.get('cantidad_consumo'),
                    'unidad_medida': data.get('unidad_medida')
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"[ConsumosAPIView] Error POST: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
