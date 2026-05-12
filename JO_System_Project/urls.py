
# JO_System_Project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
