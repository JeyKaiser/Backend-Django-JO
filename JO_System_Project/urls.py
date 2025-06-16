from django.contrib import admin
from django.urls import path, include
from costeo_app import views

#esta forma creo la lista de modulos path y los relaciono con las vistas de cada app, NO recomendado pues nos llenariamos de multiples path de diferentes apps
# esta forma seria para importar todos las vi de cada app

#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('', views.hello),
#    path('about/', views.about),
#    ]


#esta forma INCLUDE trae la lista de modulos path, que hay en cada archivo urls.py de cada app que estan relacionados a sus vistas, SI seria mejor, ya que cada app tendria su lista de urls/vista
# urlpatterns = [
#     path('admin/'   ,admin.site.urls),
#     path(''         ,include('costeo_app.urls')),
#     path('usuarios/',include('usuarios.urls'))
#     ]


urlpatterns = [
        path('admin/' ,admin.site.urls),
        path(''       ,include('usuarios.urls')),
        path('costeo/' ,include('costeo_app.urls')),
        path('sap/' ,include('sap.urls')),
    ]