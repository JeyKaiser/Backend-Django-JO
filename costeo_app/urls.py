from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

#coments
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),  
    path('index/', views.index, name='index'),
    path('coleccion/', views.RegisterReference, name='RegisterReference'),
    path('create/', views.create_collection, name='create_collection'),
    path('obtener_sublineas/<int:id_linea>/', views.obtener_sublineas, name='obtener_sublineas'),
    path('about/', views.about, name='about'),
    path('logout/', views.signout, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

