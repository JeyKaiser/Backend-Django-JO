from django.urls import path

from .views import (
    ConsumoTextilAPIView,
    FactConsumoAPIView,
    ImagesAPIView,
    ImageUploadAPIView,
    ParametrosAPIView,
    PrendasAPIView,
    SapHealthAPIView,
    SimpleDimensionListAPIView,
    SimpleProviderListAPIView,
)


def provider_view(resource_name: str):
    class View(SimpleProviderListAPIView):
        pass
    View.resource_name = resource_name
    return View.as_view()


def dimension_view(dimension_name: str):
    class View(SimpleDimensionListAPIView):
        pass
    View.dimension_name = dimension_name
    return View.as_view()


urlpatterns = [
    path('health/', SapHealthAPIView.as_view(), name='sap-health'),
    path('prendas/', PrendasAPIView.as_view(), name='sap-prendas'),
    path('images/', ImagesAPIView.as_view(), name='sap-images'),
    path('images/upload/', ImageUploadAPIView.as_view(), name='sap-image-upload'),
    path('consumo-textil/', ConsumoTextilAPIView.as_view(), name='sap-consumo-textil'),
    path('fact_consumo/', FactConsumoAPIView.as_view(), name='sap-fact-consumo'),
    path('parametros/', ParametrosAPIView.as_view(), name='sap-parametros'),
    path('parametros-view/', ParametrosAPIView.as_view(), name='sap-parametros-view'),
    path('base_textil/', provider_view('base_textil'), name='sap-base-textil'),
    path('tela/', provider_view('tela'), name='sap-tela'),
    path('print/', provider_view('print'), name='sap-print'),
    path('hilo_tela/', provider_view('hilo_tela'), name='sap-hilo-tela'),
    path('hilo_molde/', provider_view('hilo_molde'), name='sap-hilo-molde'),
    path('canal_tela/', provider_view('canal_tela'), name='sap-canal-tela'),
    path('sentido_sesgos/', provider_view('sentido_sesgos'), name='sap-sentido-sesgos'),
    path('rotacion_molde/', provider_view('rotacion_molde'), name='sap-rotacion-molde'),
    path('restricciones_tela/', provider_view('restricciones_tela'), name='sap-restricciones-tela'),
    path('dim_prenda/', dimension_view('dim_prenda'), name='sap-dim-prenda'),
    path('dim_cantidad_telas/', dimension_view('dim_cantidad_telas'), name='sap-dim-cantidad-telas'),
    path('dim_uso_tela/', dimension_view('dim_uso_tela'), name='sap-dim-uso-tela'),
    path('dim_base_textil/', dimension_view('dim_base_textil'), name='sap-dim-base-textil'),
    path('dim_caracteristica_color/', dimension_view('dim_caracteristica_color'), name='sap-dim-caracteristica-color'),
    path('dim_ancho_util/', dimension_view('dim_ancho_util'), name='sap-dim-ancho-util'),
    path('dim_propiedades_tela/', dimension_view('dim_propiedades_tela'), name='sap-dim-propiedades-tela'),
    path('dim_variante/', dimension_view('dim_variante'), name='sap-dim-variante'),
    path('dim_descripcion/', dimension_view('dim_descripcion'), name='sap-dim-descripcion'),
    path('dim_terminacion/', dimension_view('dim_terminacion'), name='sap-dim-terminacion'),
]
