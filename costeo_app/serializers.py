# serializers.py
from rest_framework import serializers
from .models import Producto, Collection, Tecnico, Tela, Creativo, Foto

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





