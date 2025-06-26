from django.contrib import admin
from django.urls import path, include
from costeo_app import views
from costeo_app.views import AnioColeccionAPIView, TestDataAPIView, ReferenciasAPIView 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView  
)



urlpatterns = [
        path('admin/' ,admin.site.urls),
        path(''       ,include('usuarios.urls')),
        path('costeo/' ,include('costeo_app.urls')),
        path('sap/' ,include('sap.urls')),

        # Rutas para la autenticación JWT (las que usará Next.js)
        # http://localhost:8000/api/token/ para obtener tokens (login)
        path("api/", include("costeo_app.urls")),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        # http://localhost:8000/api/token/refresh/ para refrescar el token de acceso
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

        path('api/colecciones/<str:coleccion>/anios/', AnioColeccionAPIView.as_view(), name='api_anio_coleccion'),       
        path('api/referencias/<str:collection_id>/', ReferenciasAPIView.as_view(), name='api_referencias'),

        path('api/test-data/<str:test_id>/', TestDataAPIView.as_view(), name='api_test_data'),
]