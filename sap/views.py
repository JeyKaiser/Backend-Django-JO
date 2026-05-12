from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SapImageAsset
from .services import SapConfigurationError, execute_hana_query, get_provider


def _image_payload(image: SapImageAsset):
    return {
        'id': image.id,
        'title': image.title,
        'image_url': image.image.url if image.image else '',
        'uploaded_at': image.uploaded_at.isoformat(),
    }


class SapHealthAPIView(APIView):
    def get(self, request):
        provider = get_provider()
        ok, message = provider.is_available()
        return Response(
            {
                'success': ok,
                'mode': settings.SAP_BACKEND_MODE,
                'message': message,
            },
            status=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class SimpleProviderListAPIView(APIView):
    resource_name = ''

    def get(self, request):
        provider = get_provider()
        getter = getattr(provider, 'get_parameter_options', None)
        if getter is None:
            return Response([], status=status.HTTP_200_OK)
        return Response(getter(self.resource_name), status=status.HTTP_200_OK)


class SimpleDimensionListAPIView(APIView):
    dimension_name = ''

    def get(self, request):
        provider = get_provider()
        getter = getattr(provider, 'get_dimension', None)
        if getter is None:
            return Response([], status=status.HTTP_200_OK)
        return Response(getter(self.dimension_name), status=status.HTTP_200_OK)


class PrendasAPIView(APIView):
    def get(self, request):
        provider = get_provider()
        return Response(provider.get_prendas(), status=status.HTTP_200_OK)


class ImagesAPIView(APIView):
    def get(self, request):
        images = [_image_payload(image) for image in SapImageAsset.objects.all()]
        return Response(images, status=status.HTTP_200_OK)


class ImageUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        title = request.data.get('title', '').strip()
        if not image_file or not title:
            return Response(
                {'error': 'Los campos image y title son requeridos'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset, created = SapImageAsset.objects.get_or_create(title=title)
        if asset.image:
            asset.image.delete(save=False)
        asset.image = image_file
        asset.save()
        return Response(_image_payload(asset), status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ParametrosAPIView(APIView):
    def get(self, request):
        provider = get_provider()
        return Response(provider.list_parametros(), status=status.HTTP_200_OK)

    def post(self, request):
        provider = get_provider()
        try:
            payload = request.data
            result = provider.create_parametro(payload)
            return Response(result, status=status.HTTP_201_CREATED)
        except SapConfigurationError as exc:
            return Response({'success': False, 'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class ConsumoTextilAPIView(APIView):
    def get(self, request):
        provider = get_provider()
        tipo_prenda = request.GET.get('tipo_prenda', '')
        cantidad_telas = request.GET.get('cantidad_telas')
        numero_variante = request.GET.get('numero_variante')
        if not tipo_prenda:
            return Response({'error': 'tipo_prenda es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        data = provider.get_consumo_textil(
            tipo_prenda=tipo_prenda,
            cantidad_telas=int(cantidad_telas) if cantidad_telas else None,
            numero_variante=numero_variante,
        )
        return Response(data, status=status.HTTP_200_OK)


class FactConsumoAPIView(APIView):
    def post(self, request):
        provider = get_provider()
        result = provider.create_fact_consumo(request.data)
        return Response(result, status=status.HTTP_201_CREATED)
