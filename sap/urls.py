
from django.urls import path
from .views import (
    GenericTableView, ParametrosAPIView, CollectionsAPIView, ParametrosViewAPIView,
    PrendasAPIView, CantidadTelasAPIView, UsoTelaAPIView, BaseTextilAPIView,
    CaracteristicaColorAPIView, AnchoUtilAPIView, PropiedadesTelaAPIView,
    VarianteAPIView, DescripcionAPIView, TerminacionAPIView,
    ImageUploadView, ImageServeView, ImageListView, ConsumoTextilAPIView,
    FactConsumoAPIView
)

# Las URLs de la app 'sap' se incluirán bajo el prefijo /api/sap/
# definido en el urls.py principal del proyecto.

urlpatterns = [
    # Endpoint para el recurso de Parámetros (GET y POST)
    path('parametros/', ParametrosAPIView.as_view(), name='parametros-list-create'),
    path('parametros-view/', ParametrosViewAPIView.as_view(), name='parametros-view-list'),

    # Endpoints para las tablas maestras (lookup tables)
    path('base_textil/', GenericTableView.as_view(), {'table_name': 'BASE_TEXTIL'}, name='base-textil-list'),
    path('print/', GenericTableView.as_view(), {'table_name': 'PRINT'}, name='print-list'),
    path('hilo_tela/', GenericTableView.as_view(), {'table_name': 'HILO_DE_TELA'}, name='hilo-tela-list'),
    path('canal_tela/', GenericTableView.as_view(), {'table_name': 'CANAL_TELA'}, name='canal-tela-list'),
    path('rotacion_molde/', GenericTableView.as_view(), {'table_name': 'ROTACION_MOLDE'}, name='rotacion-molde-list'),
    path('sentido_sesgos/', GenericTableView.as_view(), {'table_name': 'SENTIDO_SESGOS'}, name='sentido-sesgos-list'),
    path('restricciones_tela/', GenericTableView.as_view(), {'table_name': 'RESTRICCIONES_TELA'}, name='restricciones-tela-list'),
    path('hilo_molde/', GenericTableView.as_view(), {'table_name': 'HILO_DE_MOLDE'}, name='hilo-molde-list'),
    path('tela/', GenericTableView.as_view(), {'table_name': 'TELA'}, name='tela-list'),

    # --- Rutas Heredadas (si es necesario mantenerlas) ---
    # Se mantiene solo lo que aún sea relevante y no cause conflictos.
    path('collections/', CollectionsAPIView.as_view(), name='sap-collections-list'),
    path('prendas/', PrendasAPIView.as_view(), name='prendas-list'),

    # --- Rutas para Servidor de Imágenes ---
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:image_id>/', ImageServeView.as_view(), name='image-serve'),
    path('images/', ImageListView.as_view(), name='image-list'),

    # --- Rutas para Consumo Textil ---
    path('consumo-textil/', ConsumoTextilAPIView.as_view(), name='consumo-textil-list'),

    # --- Rutas para Dimensiones de Consumo Textil ---
    path('dim_prenda/', PrendasAPIView.as_view(), name='dim-prenda-list'),
    path('dim_cantidad_telas/', CantidadTelasAPIView.as_view(), name='dim-cantidad-telas-list'),
    path('dim_uso_tela/', UsoTelaAPIView.as_view(), name='dim-uso-tela-list'),
    path('dim_base_textil/', BaseTextilAPIView.as_view(), name='dim-base-textil-list'),
    path('dim_caracteristica_color/', CaracteristicaColorAPIView.as_view(), name='dim-caracteristica-color-list'),
    path('dim_ancho_util/', AnchoUtilAPIView.as_view(), name='dim-ancho-util-list'),
    path('dim_propiedades_tela/', PropiedadesTelaAPIView.as_view(), name='dim-propiedades-tela-list'),
    path('dim_variante/', VarianteAPIView.as_view(), name='dim-variante-list'),
    path('dim_descripcion/', DescripcionAPIView.as_view(), name='dim-descripcion-list'),
    path('dim_terminacion/', TerminacionAPIView.as_view(), name='dim-terminacion-list'),

    # --- Ruta para crear nuevo registro en FACT_CONSUMO ---
    path('fact_consumo/', FactConsumoAPIView.as_view(), name='fact-consumo-create'),
]
