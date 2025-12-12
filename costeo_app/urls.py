# costeo_app/urls.py
from . import views
from django.urls import path, include


# Importa solo los ViewSets si los registras aquí
#from .views import obtener_sublineas, TecnicoViewSet, TelaViewSet, CreativoViewSet, ReferenciaDetailView #ReferenciasPorAnioListView , lista_coleccion, ProductoListCreateAPIView
from .views import (ColeccionesAPIView,ReferenciasAnioAPIView, ModeloDetalleAPIView, ReferenciaDetalleAPIView, ReferenciaSearchAPIView, FasesAPIView, TrazabilidadAPIView, TrazabilidadCurrentAPIView)

# router = DefaultRouter()
# router.register(r'tecnicos', TecnicoViewSet)
# router.register(r'telas', TelaViewSet)
# router.register(r'creativos', CreativoViewSet)


urlpatterns = [    
    #colecciones endpoints
    path('colecciones/', ColeccionesAPIView.as_view(), name='api_colecciones'),
    path('referencias-por-anio/<str:collection_id>/', ReferenciasAnioAPIView.as_view(), name='referencias-por-anio-list'),
    path('referencias/search/', ReferenciaSearchAPIView.as_view(), name='api_referencia_search'),
    path('referencias/<str:codigo_referencia>/', ReferenciaDetalleAPIView.as_view(), name='api_referencia_detalle'),
    # path('referencias/', ReferenciaAPIView.as_view(), name='api_referencia_create'),
    path('referencias/<int:id_referencia>/trazabilidad/', TrazabilidadAPIView.as_view(), name='api_trazabilidad_list'),
    path('referencias/<int:id_referencia>/trazabilidad/current/', TrazabilidadCurrentAPIView.as_view(), name='api_trazabilidad_current'),
    path('detalle-referencia/<str:referencia_id>/', ModeloDetalleAPIView.as_view(), name='api_modelo_detalle'),
    path('fases/', FasesAPIView.as_view(), name='api_fases_list'),
    path('fases/<str:codigo_fase>/', FasesAPIView.as_view(), name='api_fase_detalle'),
    
    #--------paths para las vistas de Django que devuelven templates---------
    path('anio_coleccion/<str:coleccion>/', views.anio_coleccion, name='anio_coleccion'),
    path('lista_coleccion/', views.lista_coleccion, name='lista_coleccion'),
]

   