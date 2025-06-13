from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter
# from .views import obtener_sublineas ,ProductoListCreateAPIView, TecnicoViewSet, TelaViewSet, CreativoViewSet, lista_coleccion

#coments
urlpatterns = [
    path('', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'),
    path('daniel/', views.daniel, name='daniel'),
    path('danielresponde/', views.danielresponde, name='danielresponde'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)