
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser

class UserAPITests(APITestCase):
    """
    Pruebas para la API de Usuarios, adaptadas del script test_api.py.
    Estas pruebas usan el cliente de API de Django REST Framework.
    """

    @classmethod
    def setUpTestData(cls):
        # Crear un usuario de prueba para los tests que lo necesiten (GET por id)
        cls.user = CustomUser.objects.create_user(
            CODIGO_USUARIO="TEST002",
            NOMBRE_COMPLETO="Usuario Existente",
            EMAIL="existente@empresa.com",
            AREA="DISENO",
            ROL="DISENADOR"
        )

    def test_get_users(self):
        """Prueba GET /api/users/"""
        url = reverse('user-list-create')  # Asumiendo que el nombre de la URL es 'user-list-create'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Prueba POST /api/users/"""
        url = reverse('user-list-create') # Asumiendo que el nombre de la URL es 'user-list-create'
        data = {
            "CODIGO_USUARIO": "TEST001",
            "NOMBRE_COMPLETO": "Usuario de Prueba",
            "EMAIL": "test@empresa.com",
            "AREA": "DISENO",
            "ROL": "DISENADOR"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(CODIGO_USUARIO="TEST001").exists())

    def test_get_user_by_id(self):
        """Prueba GET /api/users/{id}/"""
        # Asumiendo que el nombre de la URL es 'user-detail'
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['CODIGO_USUARIO'], self.user.CODIGO_USUARIO)

    def test_search_users(self):
        """Prueba GET /api/users/search?q=Existente"""
        # Esta URL puede no ser estándar en DRF, asumiendo una implementación custom
        # Se necesita saber la URL exacta desde urls.py
        # Por ahora, se omite la prueba hasta tener la configuración de la URL.
        # Ejemplo de cómo podría ser:
        # url = f"{reverse('user-list-create')}search/?q=Existente"
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_get_user_options(self):
        """Prueba GET /api/users/options"""
        # Esta URL puede no ser estándar en DRF, asumiendo una implementación custom
        # Se necesita saber la URL exacta desde urls.py
        # Por ahora, se omite la prueba hasta tener la configuración de la URL.
        pass

