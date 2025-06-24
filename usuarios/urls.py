from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


#coments
urlpatterns = [
    path('', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'),
    # path('daniel/', views.daniel, name='daniel'),
    # path('danielresponde/', views.danielresponde, name='danielresponde'),
    #path('index/', views.index, name='index'),
    #path('login/', views.login, name='logUser'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)