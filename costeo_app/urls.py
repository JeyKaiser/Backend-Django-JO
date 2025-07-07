# costeo_app/urls.py
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa solo los ViewSets si los registras aquí
from .views import obtener_sublineas, TecnicoViewSet, TelaViewSet, CreativoViewSet, ReferenciaDetailView #ReferenciasPorAnioListView , lista_coleccion, ProductoListCreateAPIView
from .views import AnioColeccionAPIView,ReferenciasAnioAPIView, ModeloDetalleAPIView

router = DefaultRouter()
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'telas', TelaViewSet)
router.register(r'creativos', CreativoViewSet)


urlpatterns = [
    # Rutas de vistas tradicionales (si aún las usas, de lo contrario, elimínalas)
    path('index/', views.index, name='index'),
    path('coleccion/', views.collection_list, name='collection'),
    path('create/', views.create_reference, name='create_reference'),
    path('obtener_sublineas/<int:linea_id>/', views.obtener_sublineas, name='obtener_sublineas'),

    
    #años por coleccion, referencias por año, detalle de referencia
    path('colecciones/<str:coleccion>/anios/', AnioColeccionAPIView.as_view(), name='api_anio_coleccion'),
    path('referencias-por-anio/<str:collection_id>/', ReferenciasAnioAPIView.as_view(), name='referencias-por-anio-list'),
    path('modelo-detalle/<str:referencia_id>/', ModeloDetalleAPIView.as_view(), name='api_modelo_detalle'),

    path('referencias1/<str:codigo_referencia>/', ReferenciaDetailView.as_view(), name='referencia-detail'),

    path('referencias/<str:collection_id>', views.referencias, name='referencias'), # Esta es la vista basada en template

    #--------paths para las vistas de Django que devuelven templates---------
    path('anio_coleccion/<str:coleccion>/', views.anio_coleccion, name='anio_coleccion'),

    # Incluye las URLs del router para tus ViewSets
    path('', include(router.urls)), # Esto incluirá /tecnicos, /telas, /creativos directamente bajo /costeo/

]
