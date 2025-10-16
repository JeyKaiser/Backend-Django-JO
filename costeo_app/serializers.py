# # serializers.py
from rest_framework import serializers
from .models import (Producto, Collection, Tecnico, Tela, Creativo, Foto,
                     DimPrenda, DimCantidadTelas, DimUsoTela, DimBaseTextil,
                     DimCaracteristicaColor, DimAnchoUtil, DimPropiedadesTela,
                     DimVariante, DimDescripcion, DimTerminacion, FactConsumo)

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


# =====================================================================================
# SERIALIZERS PARA LA BASE DE DATOS DIMENSIONAL 'CONSUMO_TEXTIL'
# =====================================================================================

class DimPrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimPrenda
        fields = '__all__'

class DimCantidadTelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCantidadTelas
        fields = '__all__'

class DimUsoTelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimUsoTela
        fields = '__all__'

class DimBaseTextilSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimBaseTextil
        fields = '__all__'

class DimCaracteristicaColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCaracteristicaColor
        fields = '__all__'

class DimAnchoUtilSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimAnchoUtil
        fields = '__all__'

class DimPropiedadesTelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimPropiedadesTela
        fields = '__all__'

class DimVarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimVariante
        fields = '__all__'

class DimDescripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimDescripcion
        fields = '__all__'

class DimTerminacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimTerminacion
        fields = '__all__'

class FactConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactConsumo
        fields = '__all__'
