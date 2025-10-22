from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers


#----------------------------  MODELS PARA LA APLICACION DE COSTEO API REST











#----------------------------  MODELS PARA LA APLICACION DE COSTEO TEMPLATES DE DJANGO
class Tela(models.Model):
    cod_tela = models.CharField(max_length=30, null=True, blank=True)
    descripcion_tela = models.CharField(max_length=200, null=True, blank=True)
    ancho = models.CharField(max_length=50, null=True, blank=True)
    cod_color = models.CharField(max_length=30, null=True, blank=True)
    descripcion_color = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.cod_tela 

class Foto(models.Model):
    tipo_foto = models.CharField(max_length=30, null=True, blank=True)
    ruta_foto = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.tipo_foto

class Tecnico(models.Model):
    nombre_tecnico = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.nombre_tecnico

class Creativo(models.Model):
    nombre_creativo = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.nombre_creativo

class Status(models.Model):
    status = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.status

class Tipo(models.Model):
    tipo = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.tipo
    

class Variacion(models.Model):
    es_variacion = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.es_variacion or ""
        
class ColorReferencia(models.Model):
    codigo_color = models.CharField(max_length=20, null=True, blank=True)
    descripcion_color = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.codigo_color or ""

class Linea(models.Model):
    nombre_linea = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre_linea

class Sublinea(models.Model):
    nombre_sublinea = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre_sublinea

class LineaSublinea(models.Model):
    linea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    sublinea = models.ForeignKey(Sublinea, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.linea} - {self.sublinea}'


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    referencia = models.CharField(max_length=30, null=True, blank=True)
    foto_referencia = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='colecciones_foto_referencia', null=True, blank=True)
    codigo_sap_md = models.CharField(max_length=30, null=True, blank=True)
    codigo_sap_pt = models.CharField(max_length=30, null=True, blank=True)
    nombre_sistema = models.CharField(max_length=30, null=True, blank=True)
    descripcion_color = models.CharField(max_length=200, null=True, blank=True)
    codigo_color = models.CharField(max_length=20, null=True, blank=True)
    foto_tela = models.ForeignKey(Foto, on_delete=models.DO_NOTHING, related_name='colecciones_foto_tela', null=True, blank=True)
    nombre_referente = models.CharField(max_length=20, null=True, blank=True)
    linea = models.ForeignKey(Linea, on_delete=models.DO_NOTHING, related_name='colecciones_linea', null=True, blank=True)
    creativo = models.ForeignKey(Creativo, on_delete=models.DO_NOTHING, related_name='colecciones_creativo', null=True, blank=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.DO_NOTHING, related_name='colecciones_tecnico', null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='colecciones_status', null=True, blank=True)
    tallaje = models.CharField(max_length=50, null=True, blank=True)
    largo = models.CharField(max_length=50, null=True, blank=True)
    modista = models.CharField(max_length=100, null=True, blank=True)    
    def __str__(self):
        return self.referencia
    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

# =====================================================================================
# MODELOS PARA LA BASE DE DATOS DIMENSIONAL 'CONSUMO_TEXTIL'
# =====================================================================================

class DimPrenda(models.Model):
    prenda_id = models.BigAutoField(primary_key=True)
    tipo_prenda_nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_PRENDA"'

class DimCantidadTelas(models.Model):
    cantidad_telas_id = models.BigAutoField(primary_key=True)
    cantidad_telas_numero = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_CANTIDAD_TELAS"'

class DimUsoTela(models.Model):
    uso_tela_id = models.BigAutoField(primary_key=True)
    uso_tela_nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_USO_TELA"'

class DimBaseTextil(models.Model):
    base_textil_id = models.BigAutoField(primary_key=True)
    base_textil_nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_BASE_TEXTIL"'

class DimCaracteristicaColor(models.Model):
    caracteristica_color_id = models.BigAutoField(primary_key=True)
    caracteristica_nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_CARACTERISTICA_COLOR"'

class DimAnchoUtil(models.Model):
    ancho_util_id = models.BigAutoField(primary_key=True)
    ancho_util_metros = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_ANCHO_UTIL"'

class DimPropiedadesTela(models.Model):
    propiedades_tela_id = models.BigAutoField(primary_key=True)
    al_hilo_flag = models.BooleanField(default=False)
    al_sesgo_flag = models.BooleanField(default=False)
    noventa_grados_flag = models.BooleanField(default=False)
    peine_flag = models.BooleanField(default=False)
    brilloviz_flag = models.BooleanField(default=False)
    grabado_flag = models.BooleanField(default=False)
    sentido_moldes_flag = models.CharField(max_length=50)
    canal_tela_flag = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_PROPIEDADES_TELA"'

class DimVariante(models.Model):
    variante_id = models.BigAutoField(primary_key=True)
    numero_variante = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_VARIANTE"'

class DimDescripcion(models.Model):
    descripcion_id = models.BigAutoField(primary_key=True)
    detalle_descripcion = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_DESCRIPCION"'

class DimTerminacion(models.Model):
    terminacion_id = models.BigAutoField(primary_key=True)
    categoria_terminacion = models.CharField(max_length=50)
    tipo_terminacion = models.CharField(max_length=50)
    fecha_creacion = models.DateField()

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."DIM_TERMINACION"'

class FactConsumo(models.Model):
    consumo_id = models.BigAutoField(primary_key=True)
    prenda = models.ForeignKey(DimPrenda, on_delete=models.DO_NOTHING)
    cantidad_telas = models.ForeignKey(DimCantidadTelas, on_delete=models.DO_NOTHING)
    uso_tela = models.ForeignKey(DimUsoTela, on_delete=models.DO_NOTHING)
    base_textil = models.ForeignKey(DimBaseTextil, on_delete=models.DO_NOTHING)
    caracteristica_color = models.ForeignKey(DimCaracteristicaColor, on_delete=models.DO_NOTHING)
    ancho_util = models.ForeignKey(DimAnchoUtil, on_delete=models.DO_NOTHING)
    propiedades_tela = models.ForeignKey(DimPropiedadesTela, on_delete=models.DO_NOTHING)
    consumo_mtr = models.DecimalField(max_digits=10, decimal_places=4)
    variante = models.ForeignKey(DimVariante, on_delete=models.DO_NOTHING, blank=True, null=True)
    descripcion = models.ForeignKey(DimDescripcion, on_delete=models.DO_NOTHING, blank=True, null=True)
    terminacion = models.ForeignKey(DimTerminacion, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"CONSUMO_TEXTIL"."FACT_CONSUMO"'

