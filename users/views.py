import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class UsersAPIView(APIView):
    """
    API migrada desde Frontend para gestionar usuarios
    Maneja las operaciones GET y POST para usuarios (simulación sin SAP HANA)
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

            # Simulación de datos de usuarios (reemplaza con lógica real de Supabase)
            mock_users = [
                {
                    'ID_USUARIO': 1,
                    'CODIGO_USUARIO': 'USR001',
                    'NOMBRE_COMPLETO': 'Juan Pérez García',
                    'EMAIL': 'juan.perez@empresa.com',
                    'AREA': 'DISEÑO',
                    'ROL': 'DISEÑADOR',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-15'
                },
                {
                    'ID_USUARIO': 2,
                    'CODIGO_USUARIO': 'USR002',
                    'NOMBRE_COMPLETO': 'María González López',
                    'EMAIL': 'maria.gonzalez@empresa.com',
                    'AREA': 'PRODUCCION',
                    'ROL': 'CORTADOR_SENIOR',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-16'
                },
                {
                    'ID_USUARIO': 3,
                    'CODIGO_USUARIO': 'USR003',
                    'NOMBRE_COMPLETO': 'Carlos Rodríguez Martínez',
                    'EMAIL': 'carlos.rodriguez@empresa.com',
                    'AREA': 'CALIDAD',
                    'ROL': 'ESPECIALISTA_CALIDAD',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-17'
                }
            ]

            # Aplicar filtros simulados
            filtered_users = mock_users
            if area:
                filtered_users = [u for u in filtered_users if u['AREA'] == area]
            if rol:
                filtered_users = [u for u in filtered_users if u['ROL'] == rol]
            if estado:
                filtered_users = [u for u in filtered_users if u['ESTADO'] == estado]
            if search:
                search_lower = search.lower()
                filtered_users = [u for u in filtered_users if
                    search_lower in u['NOMBRE_COMPLETO'].lower() or
                    search_lower in u['CODIGO_USUARIO'].lower() or
                    search_lower in u['EMAIL'].lower()]

            # Aplicar paginación
            paginated_users = filtered_users[offset:offset + limit]

            # Preparar respuesta con estructura igual al frontend
            response_data = {
                'success': True,
                'data': paginated_users,
                'count': len(paginated_users),
                'pagination': {
                    'offset': offset,
                    'limit': limit,
                    'hasMore': len(filtered_users) > (offset + limit)
                },
                'filters': {k: v for k, v in {'area': area, 'rol': rol, 'estado': estado, 'search': search}.items() if v}
            }

            logger.info(f"[UsersAPIView] Enviando {len(paginated_users)} usuarios")
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

            # Simulación de verificación de código existente
            existing_codes = ['USR001', 'USR002', 'USR003']
            if data.get('CODIGO_USUARIO') in existing_codes:
                return Response({
                    'success': False,
                    'error': f'El código de usuario "{data.get("CODIGO_USUARIO")}" ya existe'
                }, status=status.HTTP_409_CONFLICT)

            # Simulación de creación exitosa
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

            # Simulación de búsqueda por ID
            users_db = {
                1: {
                    'ID_USUARIO': 1,
                    'CODIGO_USUARIO': 'USR001',
                    'NOMBRE_COMPLETO': 'Juan Pérez García',
                    'EMAIL': 'juan.perez@empresa.com',
                    'AREA': 'DISEÑO',
                    'ROL': 'DISEÑADOR',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-15'
                },
                2: {
                    'ID_USUARIO': 2,
                    'CODIGO_USUARIO': 'USR002',
                    'NOMBRE_COMPLETO': 'María González López',
                    'EMAIL': 'maria.gonzalez@empresa.com',
                    'AREA': 'PRODUCCION',
                    'ROL': 'CORTADOR_SENIOR',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-16'
                },
                3: {
                    'ID_USUARIO': 3,
                    'CODIGO_USUARIO': 'USR003',
                    'NOMBRE_COMPLETO': 'Carlos Rodríguez Martínez',
                    'EMAIL': 'carlos.rodriguez@empresa.com',
                    'AREA': 'CALIDAD',
                    'ROL': 'ESPECIALISTA_CALIDAD',
                    'ESTADO': 'ACTIVO',
                    'FECHA_CREACION': '2024-01-17'
                }
            }

            user = users_db.get(int(user_id))
            if not user:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'data': user
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

            # Simulación de actualización
            if not data:
                return Response({'error': 'No hay campos para actualizar'}, status=status.HTTP_400_BAD_REQUEST)

            # Simulación de actualización exitosa
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

            # Simulación de eliminación exitosa
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
        Verificar conectividad y salud de la base de datos (simulación)
        """
        try:
            logger.info("[DatabaseHealthAPIView] Verificando salud de la base de datos")

            # Simulación de verificación de salud exitosa
            return Response({
                'success': True,
                'connection': {
                    'status': 'connected',
                    'version': 'PostgreSQL 15.0',
                    'executionTime': 50
                },
                'health': [
                    {'ACTIVE_CONNECTIONS': 5},
                    {'SCHEMA_NAME': 'consumo_textil', 'TABLE_COUNT': 11}
                ],
                'timestamp': '2024-01-01T00:00:00.000Z',
                'schema': 'consumo_textil'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[DatabaseHealthAPIView] Error: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': f'Verificación de salud falló: {str(e)}',
                'timestamp': '2024-01-01T00:00:00.000Z'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)