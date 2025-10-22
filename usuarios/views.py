from .forms import CustomUserCreationForm, SigninForm
from .models import CustomUser
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


#CREAR USUARIO NUEVO
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    user = CustomUser.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1'],
                        email=request.POST['email']  # Agregar el email
                    )
                user.save()                # Iniciar sesión automáticamente después del registro
                login(request, user)
                messages.success(request, 'Cuenta creada con éxito.')
                print('Cuenta creada con éxito.')
                return redirect('signin')
            except Exception as e:
                print(f'Error: {e}')
                return render(request, 'signup.html', {'miSignup': form})
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            print('Las claves no son iguales.')
            return render(request, 'signup.html', {'miSignup': form})
    else:
        form = CustomUserCreationForm(request.POST)
        return render(request, 'signup.html', {'miSignup': form})


# Login de usuario
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'miSignin': SigninForm()
        })
    else:
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Aquí sí se llama a la función login con el usuario autenticado
                login(request, user)                
                return redirect('index')
            else:
                return render(request, 'signin.html', {
                    'miSignin': form,
                    'error': 'Usuario o Contraseña incorrecta'
                })
        else:
            return render(request, 'signin.html', {
                'miSignin': form,
                'error': 'Formulario inválido'
            })


# ============================
# API VIEWS para usuarios SAP HANA
# Compatibles con frontend Next.js
# ============================

class UsuariosAPIView(APIView):
    """
    Vista principal para gestionar usuarios
    Compatible con el frontend Next.js y API spec
    """
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        # Simulación de servicio de usuarios (reemplaza con lógica real de Supabase)
    
    def get(self, request):
        """GET /api/users/ - Lista usuarios con paginación y filtros"""
        try:
            # Parámetros de paginación
            offset = int(request.GET.get('offset', 0))
            limit = min(int(request.GET.get('limit', 50)), 100)  # Max 100
            
            # Filtros opcionales
            filters = {}
            if request.GET.get('area'):
                filters['area'] = request.GET.get('area')
            if request.GET.get('rol'):
                filters['rol'] = request.GET.get('rol')
            if request.GET.get('estado'):
                filters['estado'] = request.GET.get('estado')
            
            search_term = request.GET.get('search', '')
            
            # Simulación de obtener usuarios (reemplaza con lógica real de Supabase)
            result = {
                'users': [
                    {
                        'ID_USUARIO': 1,
                        'CODIGO_USUARIO': 'USR001',
                        'NOMBRE_COMPLETO': 'Juan Pérez',
                        'AREA': 'DISEÑO',
                        'ROL': 'DISEÑADOR',
                        'ESTADO': 'ACTIVO'
                    },
                    {
                        'ID_USUARIO': 2,
                        'CODIGO_USUARIO': 'USR002',
                        'NOMBRE_COMPLETO': 'María García',
                        'AREA': 'PRODUCCION',
                        'ROL': 'CORTADOR_SENIOR',
                        'ESTADO': 'ACTIVO'
                    }
                ],
                'total': 2
            }
            
            # Formato de respuesta según la especificación
            response_data = {
                'success': True,
                'data': result['users'],
                'count': len(result['users']),
                'pagination': {
                    'offset': offset,
                    'limit': limit,
                    'hasMore': result['total'] > (offset + limit)
                }
            }
            
            # Agregar filtros aplicados si existen
            if filters or search_term:
                response_data['filters'] = filters
                if search_term:
                    response_data['filters']['search'] = search_term
            
            logger.info(f"[UsuariosAPIView] Obtenidos {len(result['users'])} usuarios")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UsuariosAPIView] Error obteniendo usuarios: {str(e)}")
            return Response({
                'success': False,
                'error': 'Error obteniendo usuarios',
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """POST /api/users/ - Crear nuevo usuario"""
        import time
        start_time = time.time()
        
        try:
            data = request.data
            
            # Validar campos requeridos
            required_fields = ['CODIGO_USUARIO', 'NOMBRE_COMPLETO', 'AREA', 'ROL']
            for field in required_fields:
                if not data.get(field):
                    return Response({
                        'success': False,
                        'error': f'Campo requerido faltante: {field}',
                        'timestamp': self._get_timestamp()
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Simulación de verificación de usuario existente
            existing_codes = ['USR001', 'USR002']  # Simulación
            if data.get('CODIGO_USUARIO') in existing_codes:
                return Response({
                    'success': False,
                    'error': 'El código de usuario ya existe',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_409_CONFLICT)

            # Simulación de creación de usuario
            created_user = data
            execution_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"[UsuariosAPIView] Usuario creado: {data.get('CODIGO_USUARIO')}")
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': {
                    'CODIGO_USUARIO': data.get('CODIGO_USUARIO'),
                    'NOMBRE_COMPLETO': data.get('NOMBRE_COMPLETO'),
                    'AREA': data.get('AREA'),
                    'ROL': data.get('ROL'),
                    'ESTADO': data.get('ESTADO', 'ACTIVO')
                },
                'executionTime': execution_time
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            logger.error(f"[UsuariosAPIView] Error creando usuario: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat() + 'Z'


class UsuarioDetailAPIView(APIView):
    """
    Vista para gestionar un usuario específico por ID
    """
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        # Simulación de servicio de usuarios (reemplaza con lógica real de Supabase)
    
    def get(self, request, user_id):
        """GET /api/users/{id}/ - Obtener usuario por ID"""
        try:
            # Simulación de obtener usuario por ID
            users_db = {
                1: {'ID_USUARIO': 1, 'CODIGO_USUARIO': 'USR001', 'NOMBRE_COMPLETO': 'Juan Pérez'},
                2: {'ID_USUARIO': 2, 'CODIGO_USUARIO': 'USR002', 'NOMBRE_COMPLETO': 'María García'}
            }
            user = users_db.get(int(user_id))
            if user:
                return Response({
                    'success': True,
                    'data': user
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"[UsuarioDetailAPIView] Error obteniendo usuario {user_id}: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, user_id):
        """PUT /api/users/{id}/ - Actualizar usuario"""
        import time
        start_time = time.time()
        
        try:
            data = request.data
            
            # Simulación de actualización de usuario
            updated_user = data
            execution_time = int((time.time() - start_time) * 1000)
            
            if updated_user:
                logger.info(f"[UsuarioDetailAPIView] Usuario actualizado: {user_id}")
                return Response({
                    'success': True,
                    'message': 'User updated successfully',
                    'data': updated_user,
                    'executionTime': execution_time
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            logger.error(f"[UsuarioDetailAPIView] Error actualizando usuario {user_id}: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        """DELETE /api/users/{id}/ - Eliminar usuario"""
        import time
        start_time = time.time()
        
        try:
            # Verificar si es eliminación hard o soft
            hard_delete = request.GET.get('hard', 'false').lower() == 'true'
            
            # Simulación de obtener datos del usuario
            users_db = {
                1: {'ID_USUARIO': 1, 'CODIGO_USUARIO': 'USR001', 'NOMBRE_COMPLETO': 'Juan Pérez'},
                2: {'ID_USUARIO': 2, 'CODIGO_USUARIO': 'USR002', 'NOMBRE_COMPLETO': 'María García'}
            }
            user_data = users_db.get(int(user_id))
            if not user_data:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_404_NOT_FOUND)

            # Simulación de eliminación
            success = True
            execution_time = int((time.time() - start_time) * 1000)
            
            if success:
                logger.info(f"[UsuarioDetailAPIView] Usuario {'eliminado' if hard_delete else 'desactivado'}: {user_id}")
                return Response({
                    'success': True,
                    'message': 'User permanently deleted' if hard_delete else 'User deactivated successfully',
                    'deletedUser': {
                        'ID_USUARIO': user_data.get('ID_USUARIO'),
                        'CODIGO_USUARIO': user_data.get('CODIGO_USUARIO'),
                        'NOMBRE_COMPLETO': user_data.get('NOMBRE_COMPLETO')
                    },
                    'deleteType': 'hard' if hard_delete else 'soft',
                    'executionTime': execution_time
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Error eliminando usuario',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            logger.error(f"[UsuarioDetailAPIView] Error eliminando usuario {user_id}: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat() + 'Z'


class UsuariosSearchAPIView(APIView):
    """
    Vista para búsqueda avanzada de usuarios
    """
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        # Simulación de servicio de usuarios (reemplaza con lógica real de Supabase)
    
    def get(self, request):
        """GET /api/users/search/ - Búsqueda avanzada de usuarios"""
        try:
            # Parámetro de búsqueda requerido
            search_term = request.GET.get('q', '')
            if not search_term:
                return Response({
                    'success': False,
                    'error': 'Parámetro de búsqueda "q" es requerido',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Filtros adicionales
            filters = {}
            if request.GET.get('area'):
                filters['area'] = request.GET.get('area')
            if request.GET.get('rol'):
                filters['rol'] = request.GET.get('rol')
            if request.GET.get('estado'):
                filters['estado'] = request.GET.get('estado')
            
            # Configuraciones de búsqueda
            exact_match = request.GET.get('exact', 'false').lower() == 'true'
            limit = min(int(request.GET.get('limit', 20)), 50)  # Max 50
            
            # Simulación de búsqueda de usuarios
            results = [
                {
                    'ID_USUARIO': 1,
                    'CODIGO_USUARIO': 'USR001',
                    'NOMBRE_COMPLETO': f'Resultado para "{search_term}"',
                    'AREA': 'DISEÑO',
                    'ROL': 'DISEÑADOR'
                }
            ]
            
            # Generar sugerencias simples
            suggestions = [user.get('NOMBRE_COMPLETO', '') for user in results[:3]]
            
            logger.info(f"[UsuariosSearchAPIView] Búsqueda '{search_term}': {len(results)} resultados")
            return Response({
                'success': True,
                'data': results,
                'count': len(results),
                'searchType': 'exact' if exact_match else 'general',
                'query': search_term,
                'filters': filters,
                'suggestions': suggestions
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UsuariosSearchAPIView] Error en búsqueda: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat() + 'Z'


class UsuariosOptionsAPIView(APIView):
    """
    Vista para obtener opciones de campos (roles, estados, etc.)
    """
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        # Simulación de servicio de usuarios (reemplaza con lógica real de Supabase)
    
    def get(self, request):
        """GET /api/users/options/ - Opciones de campos y estadísticas"""
        try:
            # Simulación de opciones de usuario
            options = {
                'currentAreas': ['DISEÑO', 'PRODUCCION', 'CALIDAD'],
                'currentRoles': ['DISEÑADOR', 'CORTADOR_SENIOR', 'ANALISTA_COSTOS'],
                'statusCounts': [
                    {'estado': 'ACTIVO', 'count': 15},
                    {'estado': 'INACTIVO', 'count': 2}
                ]
            }
            
            # Formato según especificación
            response_data = {
                'success': True,
                'data': {
                    'currentAreas': options.get('currentAreas', []),
                    'currentRoles': options.get('currentRoles', []),
                    'statusCounts': options.get('statusCounts', []),
                    'validAreas': [
                        'DISEÑO', 'PRODUCCION', 'CALIDAD', 'TECNICO', 
                        'PATRONAJE', 'COMERCIAL', 'OPERACIONES'
                    ],
                    'validRoles': [
                        'JEFE_OPERACIONES', 'DISEÑADOR_SENIOR', 'DISEÑADOR',
                        'CORTADOR_SENIOR', 'ESPECIALISTA_CALIDAD', 'INGENIERO_TEXTIL',
                        'PATRONISTA_SENIOR', 'ANALISTA_COSTOS'
                    ],
                    'validEstados': ['ACTIVO', 'INACTIVO'],
                    'roleDescriptions': {
                        'JEFE_OPERACIONES': 'Responsable de operaciones generales',
                        'DISEÑADOR_SENIOR': 'Diseñador con experiencia senior',
                        'DISEÑADOR': 'Diseñador de prendas',
                        'CORTADOR_SENIOR': 'Especialista en corte senior',
                        'ESPECIALISTA_CALIDAD': 'Control y aseguramiento de calidad',
                        'INGENIERO_TEXTIL': 'Especialista técnico en textiles',
                        'PATRONISTA_SENIOR': 'Especialista en patronaje senior',
                        'ANALISTA_COSTOS': 'Análisis de costos y pricing'
                    },
                    'areaDescriptions': {
                        'DISEÑO': 'Área de diseño y desarrollo creativo',
                        'PRODUCCION': 'Área de producción y manufactura',
                        'CALIDAD': 'Control y aseguramiento de calidad',
                        'TECNICO': 'Área técnica y de ingeniería',
                        'PATRONAJE': 'Desarrollo de patrones y molería',
                        'COMERCIAL': 'Área comercial y de costos',
                        'OPERACIONES': 'Operaciones generales y coordinación'
                    }
                },
                'timestamp': self._get_timestamp()
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"[UsuariosOptionsAPIView] Error obteniendo opciones: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat() + 'Z'


# ============================
# Views adicionales para testing
# ============================

@api_view(['GET'])
@permission_classes([AllowAny])
def test_hana_connection(request):
    """
    Vista para probar la conexión con SAP HANA
    """
    try:
        # Simulación de conexión exitosa
        return Response({
            'status': 'success',
            'message': 'Conexión simulada exitosa con base de datos',
            'total_users': 2
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"[test_connection] Error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Error conectando con base de datos: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

