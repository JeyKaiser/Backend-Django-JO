import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sap.services import get_provider

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
            
            provider = get_provider()
            data = provider.get_consumos_by_reference(reference)

            if data is None:
                logger.error("[ConsumosAPIView] Error de BD: proveedor SAP no disponible")
                return Response({
                    'success': False,
                    'error': 'Error de base de datos: proveedor SAP no disponible',
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
            
            provider = get_provider()
            provider.create_consumo({
                'referencia': data.get('referencia'),
                'codigo_tela': data.get('codigo_tela'),
                'cantidad_consumo': data.get('cantidad_consumo'),
                'unidad_medida': data.get('unidad_medida')
            })
            
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
