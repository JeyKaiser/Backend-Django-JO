from django.urls import path
from .views import ConsumosAPIView

urlpatterns = [
    # API de consumos de telas
    path('', ConsumosAPIView.as_view(), name='consumos-list-create'),
]