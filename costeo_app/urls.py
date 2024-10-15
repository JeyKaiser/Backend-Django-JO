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
    #path('proyecto/', views.proyecto, name='proyecto'),
    #path('proyecto/<int:id>', views.project_detail, name='project_detail'),
    #path('tasks/', views.tasks, name='tasks'),
    #path('create_task/', views.create_task, name='create_task'),
    #path('create_project/', views.create_project, name='create_project'),   
    path('about/', views.about, name='about'),
    path('logout/', views.signout, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

