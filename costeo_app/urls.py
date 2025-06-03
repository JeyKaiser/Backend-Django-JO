from . import views
from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from costeo_app.views import ProductoListCreateAPIView  # ✅ Este sí existe


#coments
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),  
    path('index/', views.index, name='index'),
    path('coleccion/', views.lista_Referencias, name='collection'),
    path('create/', views.create_reference, name='create_reference'),
    path('obtener_sublineas/<int:id_linea>/', views.obtener_sublineas, name='obtener_sublineas'),
    path('about/', views.about, name='about'),
    path('logout/', views.signout, name='logout'),
    path('api/productos/', ProductoListCreateAPIView.as_view(), name='producto-list-create'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

