
# JO_System_Project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importaciones de vistas específicas que se mantienen en las rutas principales
from costeo_app.views import (
    ColeccionesAPIView,
    PTSearchAPIView,
    TestDataAPIView,
    lista_coleccion,
)


# Importaciones JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- APIS PRINCIPALES Y DE OTRAS APPS ---
    path('', include('usuarios.urls')),
    path('costeo/', include('costeo_app.urls')),
    path('api/', include('costeo_app.urls')),

    # --- NUEVA RUTA UNIFICADA PARA LA APP SAP ---
    # Todas las rutas definidas en sap.urls (parametros, base_textil, etc.)
    # estarán disponibles bajo /api/sap/
    path('api/sap/', include('sap.urls')),
    
    # --- NUEVAS APPS MIGRADAS DESDE FRONTEND ---
    path('api/users/', include('users.urls')),
    path('api/consumos/', include('consumos.urls')),

    # --- RUTAS DE API CENTRALIZADAS (LEGACY O ESPECÍFICAS) ---
    # Autenticación JWT
    # --- RUTAS DE AUTENTICACIÓN Y API ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # APIs de búsqueda y productos (se mantienen si son de costeo_app)
    path('api/search-pt/', PTSearchAPIView.as_view(), name='api_search_pt_code'),
    path('api/colecciones/', ColeccionesAPIView.as_view(), name='api_colecciones'),
    path('api/colecciones-list/', lista_coleccion, name='api_coleccion_list'),

    # API de Prueba
    path('api/test-data/<str:test_id>/', TestDataAPIView.as_view(), name='api_test_data'),
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
