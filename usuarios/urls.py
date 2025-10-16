from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


#coments
urlpatterns = [
    # URLs originales
    path('', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'),
    # path('daniel/', views.daniel, name='daniel'),
    # path('danielresponde/', views.danielresponde, name='danielresponde'),
    #path('index/', views.index, name='index'),
    #path('login/', views.login, name='logUser'),
    
    # ============================
    # API URLs para usuarios SAP HANA
    # Compatibles con USER_MANAGEMENT_API especificación
    # ============================
    
    # URLs de opciones y búsqueda (DEBEN ir antes que las de detalle para evitar conflictos)
    path('api/users/search', views.UsuariosSearchAPIView.as_view(), name='usuarios-search-api'),
    path('api/users/options', views.UsuariosOptionsAPIView.as_view(), name='usuarios-options-api'),
    
    # URL principal para usuarios (GET: lista, POST: crear)
    path('api/users', views.UsuariosAPIView.as_view(), name='usuarios-api'),
    
    # URL para usuario específico por ID (GET, PUT, DELETE)
    path('api/users/<int:user_id>', views.UsuarioDetailAPIView.as_view(), name='usuario-detail-api'),
    
    # URL para test de conexión HANA
    path('api/test-hana/', views.test_hana_connection, name='test-hana-connection'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)