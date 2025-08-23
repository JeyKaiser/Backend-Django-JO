from . import views
from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
#from rest_framework.routers import DefaultRouter



#coments
urlpatterns = [
    path('models/', views.models, name='models'),
    path('collections/', views.CollectionsAPIView.as_view(), name='collections'),
    path('', views.ConsumosAPIView.as_view(), name='consumos'),  # Endpoint directo para /api/consumos/
]

