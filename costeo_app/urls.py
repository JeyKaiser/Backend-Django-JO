# costeo_app/urls.py
from . import views
from django.urls import path, include


# Importa solo los ViewSets si los registras aquí
#from .views import obtener_sublineas, TecnicoViewSet, TelaViewSet, CreativoViewSet, ReferenciaDetailView #ReferenciasPorAnioListView , lista_coleccion, ProductoListCreateAPIView
from .views import ColeccionesAPIView, AnioColeccionAPIView,ReferenciasAnioAPIView, ModeloDetalleAPIView, FasesDeReferenciaAPIView, FaseDetalleAPIView, ReferenciaDetalleAPIView, ReferenciaSearchAPIView, ReferenciaAPIView, FasesAPIView, TrazabilidadAPIView, TrazabilidadCurrentAPIView

# router = DefaultRouter()
# router.register(r'tecnicos', TecnicoViewSet)
# router.register(r'telas', TelaViewSet)
# router.register(r'creativos', CreativoViewSet)


urlpatterns = [
    # Rutas de vistas tradicionales
    path('index/', views.index, name='index'),
    path('coleccion/', views.collection_list, name='collection'),
    path('create/', views.create_reference, name='create_reference'),
    path('obtener_sublineas/<int:linea_id>/', views.obtener_sublineas, name='obtener_sublineas'),

    
    #colecciones endpoints
    path('colecciones/', ColeccionesAPIView.as_view(), name='api_colecciones'),
    path('colecciones/<str:coleccion>/anios/', AnioColeccionAPIView.as_view(), name='api_anio_coleccion'),
    path('anio_coleccion/<str:coleccion>/anios/', AnioColeccionAPIView.as_view(), name='api_anio_coleccion_alt'),
    path('referencias-por-anio/<str:collection_id>/', ReferenciasAnioAPIView.as_view(), name='referencias-por-anio-list'),
    path('referencias/search/', ReferenciaSearchAPIView.as_view(), name='api_referencia_search'),
    path('referencias/<str:codigo_referencia>/', ReferenciaDetalleAPIView.as_view(), name='api_referencia_detalle'),
    path('referencias/', ReferenciaAPIView.as_view(), name='api_referencia_create'),
    path('fases/', FasesAPIView.as_view(), name='api_fases_list'),
    path('fases/<str:codigo_fase>/', FasesAPIView.as_view(), name='api_fase_detalle'),
    path('referencias/<int:id_referencia>/trazabilidad/', TrazabilidadAPIView.as_view(), name='api_trazabilidad_list'),
    path('referencias/<int:id_referencia>/trazabilidad/current/', TrazabilidadCurrentAPIView.as_view(), name='api_trazabilidad_current'),
    path('detalle-referencia/<str:referencia_id>/', ModeloDetalleAPIView.as_view(), name='api_modelo_detalle'),
    path('fases/<str:collection_id>/<str:referencia_id>/<str:fasesSlug>/', FasesDeReferenciaAPIView.as_view(), name='api_fase_detalle'),
    path('fases/<str:fase_slug>/<str:referencia_id>/', FaseDetalleAPIView.as_view(), name='api_fase_detalle'),
    

    #path('referencias1/<str:codigo_referencia>/', ReferenciaDetailView.as_view(), name='referencia-detail'),

    #--------paths para las vistas de Django que devuelven templates---------
    path('anio_coleccion/<str:coleccion>/', views.anio_coleccion, name='anio_coleccion'),

    # Incluye las URLs del router para tus ViewSets
    #path('', include(router.urls)), # Esto incluirá /tecnicos, /telas, /creativos directamente bajo /costeo/

]
