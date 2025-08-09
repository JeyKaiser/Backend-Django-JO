# JO_System_Project/urls.py
from django.contrib import admin
from django.urls import path, include
from costeo_app import views 
from django.conf import settings
from django.conf.urls.static import static

# Importa TODAS tus clases de APIView directamente aquí
from costeo_app.views import (
    AnioColeccionAPIView,
    TestDataAPIView,   
    PTSearchAPIView,    
    ModeloDetalleAPIView,
    lista_coleccion, # Si es una función/vista de API que quieres en la ruta principal
)

# Importaciones JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),          # Rutas de la app usuarios (ej. login tradicional si existe)
    path('costeo/', include('costeo_app.urls')), # Rutas de la app costeo_app (solo si tiene vistas no-API o sub-APIs específicas)
    path('sap/', include('sap.urls')),           # Rutas de la app sap
    path('api/', include('costeo_app.urls')),

    # --- RUTAS DE API CENTRALIZADAS PARA NEXT.JS ---
    # Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # APIs de búsqueda y productos
    path('api/search-pt/', PTSearchAPIView.as_view(), name='api_search_pt_code'),
    #path('api/productos/', ProductoListCreateAPIView.as_view(), name='api_producto_list_create'),
    path('api/colecciones-list/', lista_coleccion, name='api_coleccion_list'), # Renombrado para evitar conflicto con /colecciones/<str:coleccion>/anios/

    # API de Prueba (la que ya funciona)
    path('api/test-data/<str:test_id>/', TestDataAPIView.as_view(), name='api_test_data'),

    # Si usas el router para ViewSets, inclúyelo aquí
    #path('api/', include(router.urls)), # Esto incluirá /api/tecnicos, /api/telas, etc.
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)