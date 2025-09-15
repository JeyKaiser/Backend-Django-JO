
from django.urls import path
from .views import GenericTableView, ParametrosAPIView, CollectionsAPIView

# Las URLs de la app 'sap' se incluirán bajo el prefijo /api/sap/
# definido en el urls.py principal del proyecto.

urlpatterns = [
    # Endpoint para el recurso de Parámetros (GET y POST)
    path('parametros/', ParametrosAPIView.as_view(), name='parametros-list-create'),

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
]
