# # serializers.py
from rest_framework import serializers
from .models import Producto, Collection, Tecnico, Tela, Creativo, Foto

# class ReferenciaSerializer(serializers.ModelSerializer):
#     # Añade un campo para las fases disponibles usando la propiedad del modelo
#     fases_disponibles = serializers.SerializerMethodField()

#     class Meta:
#         model = Referencia
#         fields = ['codigo_referencia', 'nombre', 'imagen_url', 'fases_disponibles'] # Añade 'imagen_url' si la tienes

#     def get_fases_disponibles(self, obj):
#         return obj.fases_disponibles














#---------------------------- SERIALIZERS PARA LA APLICACION DE COSTEO TEMPLATES DE DJANGO
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'

class TelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tela
        fields = '__all__'
    
class CreativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creativo
        fields = '__all__'


