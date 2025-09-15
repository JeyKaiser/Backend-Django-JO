from .forms import CustomUserCreationForm, SigninForm
from .models import CustomUser
from .hana_service import UsuariosHanaService
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
        self.usuarios_service = UsuariosHanaService()
    
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
            
            # Obtener usuarios
            result = self.usuarios_service.get_all_users(
                limit=limit, 
                offset=offset, 
                filters=filters,
                search=search_term
            )
            
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
            
            # Verificar que el código de usuario no exista
            existing_user = self.usuarios_service.get_user_by_code(data.get('CODIGO_USUARIO'))
            if existing_user:
                return Response({
                    'success': False,
                    'error': 'El código de usuario ya existe',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_409_CONFLICT)
            
            # Crear usuario
            created_user = self.usuarios_service.create_user(data)
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
        self.usuarios_service = UsuariosHanaService()
    
    def get(self, request, user_id):
        """GET /api/users/{id}/ - Obtener usuario por ID"""
        try:
            user = self.usuarios_service.get_user_by_id(int(user_id))
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
            
            # Actualizar solo los campos proporcionados
            updated_user = self.usuarios_service.update_user(int(user_id), data)
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
            
            # Obtener datos del usuario antes de eliminar
            user_data = self.usuarios_service.get_user_by_id(int(user_id))
            if not user_data:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado',
                    'timestamp': self._get_timestamp()
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Realizar la eliminación
            success = self.usuarios_service.delete_user(int(user_id), hard_delete)
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
        self.usuarios_service = UsuariosHanaService()
    
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
            
            results = self.usuarios_service.search_users(
                search_term, 
                filters, 
                exact_match=exact_match, 
                limit=limit
            )
            
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
        self.usuarios_service = UsuariosHanaService()
    
    def get(self, request):
        """GET /api/users/options/ - Opciones de campos y estadísticas"""
        try:
            options = self.usuarios_service.get_user_options()
            
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
        usuarios_service = UsuariosHanaService()
        test_query = f"SELECT COUNT(*) as total FROM {usuarios_service.table_name}"
        result = usuarios_service.hana.execute_query(test_query)
        
        return Response({
            'status': 'success',
            'message': 'Conexión exitosa con SAP HANA',
            'total_users': result[0]['TOTAL'] if result else 0
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"[test_hana_connection] Error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Error conectando con SAP HANA: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

