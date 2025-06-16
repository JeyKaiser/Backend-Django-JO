from . import views
from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
#from rest_framework.routers import DefaultRouter



#coments
urlpatterns = [
    # path('', views.signup, name='signup'),
    # path('signin/', views.signin, name='signin'),  
    #path('', views.index, name='indexeee'),
    path('models/', views.models, name='models'),
]

