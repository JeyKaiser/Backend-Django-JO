# costeo_app/urls.py
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa solo los ViewSets si los registras aquí
from .views import obtener_sublineas, TecnicoViewSet, TelaViewSet, CreativoViewSet #, lista_coleccion, ProductoListCreateAPIView

router = DefaultRouter()
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'telas', TelaViewSet)
router.register(r'creativos', CreativoViewSet)



urlpatterns = [
    # Rutas de vistas tradicionales (si aún las usas, de lo contrario, elimínalas)
    path('index/', views.index, name='index'),
    path('coleccion/', views.collection_list, name='collection'),
    path('anio_coleccion/<str:coleccion>/', views.anio_coleccion, name='anio_coleccion'), # Esta es la vista basada en template
    path('referencias/<str:collection_id>', views.referencias, name='referencias'), # Esta es la vista basada en template
    path('create/', views.create_reference, name='create_reference'),
    path('obtener_sublineas/<int:linea_id>/', views.obtener_sublineas, name='obtener_sublineas'),

    # Incluye las URLs del router para tus ViewSets
    path('', include(router.urls)), # Esto incluirá /tecnicos, /telas, /creativos directamente bajo /costeo/
   
]
