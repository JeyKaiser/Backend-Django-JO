from django.urls import path
from .views import UsersAPIView, UserDetailAPIView, DatabaseHealthAPIView

urlpatterns = [
    # API de usuarios
    path('', UsersAPIView.as_view(), name='users-list-create'),
    path('<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    
    # API de salud de la base de datos
    path('database/health/', DatabaseHealthAPIView.as_view(), name='database-health'),
]