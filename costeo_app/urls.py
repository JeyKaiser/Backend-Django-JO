from . import views
from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import obtener_sublineas ,ProductoListCreateAPIView, TecnicoViewSet, TelaViewSet, CreativoViewSet, lista_coleccion


router = DefaultRouter()
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'telas', TelaViewSet)
router.register(r'creativos', CreativoViewSet)
#router.register(r'productos', ProductoListCreateAPIView, basename='producto')
#router.register(r'colecciones', lista_coleccion, basename='coleccion')


#coments
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),  
    path('index/', views.index, name='index'),
    path('coleccion/', views.lista_Referencias, name='collection'),
    path('create/', views.create_reference, name='create_reference'),
    path('obtener_sublineas/<int:linea_id>/', views.obtener_sublineas, name='obtener_sublineas'),
    path('about/', views.about, name='about'),
    path('logout/', views.signout, name='logout'),

    path('api/', include(router.urls)),
    path('api/colecciones/', lista_coleccion),
    path('api/index1/', ProductoListCreateAPIView.as_view(), name='index1'),    
    path('api/productos/', ProductoListCreateAPIView.as_view(), name='producto-list-create'),    
    path('indexJO/', views.indexJO, name='indexJO'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

