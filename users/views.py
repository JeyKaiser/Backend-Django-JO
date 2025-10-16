import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sap.views import execute_hana_query

logger = logging.getLogger(__name__)

class UsersAPIView(APIView):
    """
    API migrada desde Frontend para gestionar usuarios
    Maneja las operaciones GET y POST para usuarios en SAP HANA
    """
    def get(self, request):
        """
        Obtener usuarios con filtros opcionales y paginación
        """
        try:
            # Obtener parámetros de consulta
            offset = int(request.GET.get('offset', 0))
            limit = min(int(request.GET.get('limit', 50)), 100)
            
            # Filtros opcionales
            area = request.GET.get('area')
            rol = request.GET.get('rol') 
            estado = request.GET.get('estado')
            search = request.GET.get('search')
            
            logger.info(f"[UsersAPIView] GET usuarios: offset={offset}, limit={limit}, filtros: area={area}, rol={rol}, estado={estado}, search={search}")
            
            # Construir consulta SQL con filtros
            sql = """
                SELECT 
                    ID_USUARIO,
                    CODIGO_USUARIO,
                    NOMBRE_COMPLETO,
                    EMAIL,
                    AREA,
                    ROL,
                    ESTADO,
                    FECHA_CREACION
                FROM GARMENT_PRODUCTION_CONTROL.T_USUARIOS
                WHERE 1=1
            """
            
            params = []
            
            # Aplicar filtros
            if area:
                sql += " AND AREA = ?"
                params.append(area)
                
            if rol:
                sql += " AND ROL = ?"
                params.append(rol)
                
            if estado:
                sql += " AND ESTADO = ?"
                params.append(estado)
                
            if search:
                sql += " AND (NOMBRE_COMPLETO LIKE ? OR CODIGO_USUARIO LIKE ? OR EMAIL LIKE ?)"
                search_term = f"%{search}%"
                params.extend([search_term, search_term, search_term])
            
            # Agregar ordenamiento y paginación
            sql += " ORDER BY NOMBRE_COMPLETO ASC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            # Ejecutar consulta
            data, error = execute_hana_query(sql, params, schema='GARMENT_PRODUCTION_CONTROL')
            
            if error:
                logger.error(f"[UsersAPIView] Error de BD: {error}")
                return Response({'error': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Preparar respuesta con estructura igual al frontend
            response_data = {
                'success': True,
                'data': data or [],
                'count': len(data or []),
                'pagination': {
                    'offset': offset,
                    'limit': limit,
                    'hasMore': len(data or []) == limit
                },
                'filters': {k: v for k, v in {'area': area, 'rol': rol, 'estado': estado, 'search': search}.items() if v}
            }
            
            logger.info(f"[UsersAPIView] Enviando {len(data or [])} usuarios")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UsersAPIView] Error: {e}", exc_info=True)
            return Response({'error': f'Error interno: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """
        Crear nuevo usuario
        """
        try:
            data = request.data
            logger.info(f"[UsersAPIView] POST crear usuario: {data.get('CODIGO_USUARIO', 'N/A')}")
            
            # Validar campos requeridos
            required_fields = ['CODIGO_USUARIO', 'NOMBRE_COMPLETO', 'AREA', 'ROL']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return Response({
                    'success': False,
                    'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar áreas y roles válidos
            valid_areas = ['DISEÑO', 'PRODUCCION', 'CALIDAD', 'TECNICO', 'PATRONAJE', 'COMERCIAL', 'OPERACIONES']
            valid_roles = [
                'JEFE_OPERACIONES', 'DISEÑADOR_SENIOR', 'DISEÑADOR', 'CORTADOR_SENIOR', 
                'ESPECIALISTA_CALIDAD', 'INGENIERO_TEXTIL', 'PATRONISTA_SENIOR', 'ANALISTA_COSTOS'
            ]
            
            if data.get('AREA') not in valid_areas:
                return Response({
                    'success': False,
                    'error': f'Área inválida. Áreas válidas: {", ".join(valid_areas)}'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if data.get('ROL') not in valid_roles:
                return Response({
                    'success': False,
                    'error': f'Rol inválido. Roles válidos: {", ".join(valid_roles)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el código de usuario ya existe
            check_sql = """
                SELECT COUNT(*) as count FROM GARMENT_PRODUCTION_CONTROL.T_USUARIOS 
                WHERE CODIGO_USUARIO = ?
            """
            check_data, check_error = execute_hana_query(check_sql, [data.get('CODIGO_USUARIO')], schema='GARMENT_PRODUCTION_CONTROL')
            
            if check_error:
                return Response({'error': f'Error verificando código: {check_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            if check_data and check_data[0].get('count', 0) > 0:
                return Response({
                    'success': False,
                    'error': f'El código de usuario "{data.get("CODIGO_USUARIO")}" ya existe'
                }, status=status.HTTP_409_CONFLICT)
            
            # Crear usuario
            create_sql = """
                INSERT INTO GARMENT_PRODUCTION_CONTROL.T_USUARIOS (
                    CODIGO_USUARIO, NOMBRE_COMPLETO, EMAIL, AREA, ROL, ESTADO
                ) VALUES (?, ?, ?, ?, ?, ?)
            """
            
            params = [
                data.get('CODIGO_USUARIO'),
                data.get('NOMBRE_COMPLETO'),
                data.get('EMAIL', None),
                data.get('AREA'),
                data.get('ROL'),
                data.get('ESTADO', 'ACTIVO')
            ]
            
            result_data, create_error = execute_hana_query(create_sql, params, schema='GARMENT_PRODUCTION_CONTROL')
            
            if create_error:
                logger.error(f"[UsersAPIView] Error creando usuario: {create_error}")
                return Response({'error': f'Error creando usuario: {create_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            logger.info(f"[UsersAPIView] Usuario {data.get('CODIGO_USUARIO')} creado exitosamente")
            return Response({
                'success': True,
                'message': 'Usuario creado exitosamente',
                'data': {
                    'CODIGO_USUARIO': data.get('CODIGO_USUARIO'),
                    'NOMBRE_COMPLETO': data.get('NOMBRE_COMPLETO'),
                    'EMAIL': data.get('EMAIL'),
                    'AREA': data.get('AREA'),
                    'ROL': data.get('ROL'),
                    'ESTADO': data.get('ESTADO', 'ACTIVO')
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"[UsersAPIView] Error POST: {e}", exc_info=True)
            return Response({'error': f'Error interno: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailAPIView(APIView):
    """
    API para operaciones sobre usuarios individuales
    """
    def get(self, request, user_id):
        """
        Obtener usuario por ID
        """
        try:
            logger.info(f"[UserDetailAPIView] GET usuario ID: {user_id}")
            
            sql = """
                SELECT * FROM GARMENT_PRODUCTION_CONTROL.T_USUARIOS 
                WHERE ID_USUARIO = ?
            """
            
            data, error = execute_hana_query(sql, [user_id], schema='GARMENT_PRODUCTION_CONTROL')
            
            if error:
                return Response({'error': f'Error de base de datos: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            if not data:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'success': True,
                'data': data[0]
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UserDetailAPIView] Error GET: {e}", exc_info=True)
            return Response({'error': f'Error interno: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, user_id):
        """
        Actualizar usuario
        """
        try:
            data = request.data
            logger.info(f"[UserDetailAPIView] PUT usuario ID: {user_id}")
            
            # Construir consulta de actualización dinámica
            update_fields = []
            params = []
            
            for field in ['CODIGO_USUARIO', 'NOMBRE_COMPLETO', 'EMAIL', 'AREA', 'ROL', 'ESTADO']:
                if field in data:
                    update_fields.append(f"{field} = ?")
                    params.append(data[field])
            
            if not update_fields:
                return Response({'error': 'No hay campos para actualizar'}, status=status.HTTP_400_BAD_REQUEST)
            
            params.append(user_id)
            
            sql = f"""
                UPDATE GARMENT_PRODUCTION_CONTROL.T_USUARIOS 
                SET {', '.join(update_fields)}
                WHERE ID_USUARIO = ?
            """
            
            result_data, error = execute_hana_query(sql, params, schema='GARMENT_PRODUCTION_CONTROL')
            
            if error:
                return Response({'error': f'Error actualizando usuario: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': 'Usuario actualizado exitosamente'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UserDetailAPIView] Error PUT: {e}", exc_info=True)
            return Response({'error': f'Error interno: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, user_id):
        """
        Eliminar usuario (soft delete)
        """
        try:
            logger.info(f"[UserDetailAPIView] DELETE usuario ID: {user_id}")
            
            sql = """
                UPDATE GARMENT_PRODUCTION_CONTROL.T_USUARIOS 
                SET ESTADO = 'INACTIVO'
                WHERE ID_USUARIO = ?
            """
            
            result_data, error = execute_hana_query(sql, [user_id], schema='GARMENT_PRODUCTION_CONTROL')
            
            if error:
                return Response({'error': f'Error eliminando usuario: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': 'Usuario eliminado exitosamente'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UserDetailAPIView] Error DELETE: {e}", exc_info=True)
            return Response({'error': f'Error interno: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DatabaseHealthAPIView(APIView):
    """
    API migrada desde Frontend para verificar salud de la base de datos
    """
    def get(self, request):
        """
        Verificar conectividad y salud de SAP HANA
        """
        try:
            logger.info("[DatabaseHealthAPIView] Verificando salud de la base de datos")
            
            # Test básico de conexión
            test_sql = "SELECT VERSION FROM M_DATABASE"
            test_data, test_error = execute_hana_query(test_sql, schema='GARMENT_PRODUCTION_CONTROL')
            
            if test_error:
                logger.error(f"[DatabaseHealthAPIView] Error de conexión: {test_error}")
                return Response({
                    'success': False,
                    'error': test_error,
                    'timestamp': '2024-01-01T00:00:00.000Z'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            # Consultas adicionales de salud
            health_queries = [
                "SELECT COUNT(*) as ACTIVE_CONNECTIONS FROM M_CONNECTIONS WHERE CONNECTION_STATUS = 'RUNNING'",
                "SELECT SCHEMA_NAME, COUNT(*) as TABLE_COUNT FROM TABLES WHERE SCHEMA_NAME = 'GARMENT_PRODUCTION_CONTROL' GROUP BY SCHEMA_NAME"
            ]
            
            health_results = []
            for sql in health_queries:
                result, error = execute_hana_query(sql, schema='GARMENT_PRODUCTION_CONTROL')
                if not error and result:
                    health_results.append(result)
            
            version = test_data[0].get('VERSION', 'unknown') if test_data else 'unknown'
            
            return Response({
                'success': True,
                'connection': {
                    'status': 'connected',
                    'version': version,
                    'executionTime': 50  # Tiempo estimado
                },
                'health': health_results,
                'timestamp': '2024-01-01T00:00:00.000Z',
                'schema': 'GARMENT_PRODUCTION_CONTROL'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[DatabaseHealthAPIView] Error: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': f'Verificación de salud falló: {str(e)}',
                'timestamp': '2024-01-01T00:00:00.000Z'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)