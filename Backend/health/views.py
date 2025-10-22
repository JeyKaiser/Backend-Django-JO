from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import psycopg2


class HealthCheckView(APIView):
    """
    API para verificar la salud del backend y base de datos
    """
    def get(self, request):
        """
        Verificar conectividad y salud del sistema
        """
        try:
            health_status = {
                'status': 'healthy',
                'timestamp': '2024-01-01T00:00:00.000Z',
                'services': {}
            }

            # Verificar base de datos
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1 as test")
                    result = cursor.fetchone()
                    if result and result[0] == 1:
                        health_status['services']['database'] = {
                            'status': 'connected',
                            'type': 'PostgreSQL'
                        }
                    else:
                        health_status['services']['database'] = {
                            'status': 'error',
                            'message': 'Database query failed'
                        }
            except Exception as db_error:
                health_status['services']['database'] = {
                    'status': 'error',
                    'message': str(db_error)
                }
                health_status['status'] = 'unhealthy'

            # Verificar esquema consumo_textil
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) as table_count
                        FROM information_schema.tables
                        WHERE table_schema = 'consumo_textil'
                    """)
                    result = cursor.fetchone()
                    table_count = result[0] if result else 0

                    health_status['services']['consumo_textil_schema'] = {
                        'status': 'available' if table_count > 0 else 'empty',
                        'table_count': table_count
                    }
            except Exception as schema_error:
                health_status['services']['consumo_textil_schema'] = {
                    'status': 'error',
                    'message': str(schema_error)
                }

            # Información del sistema
            health_status['services']['backend'] = {
                'status': 'running',
                'framework': 'Django',
                'version': '4.2+'
            }

            response_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE

            return Response(health_status, status=response_status)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Health check failed: {str(e)}',
                'timestamp': '2024-01-01T00:00:00.000Z'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)