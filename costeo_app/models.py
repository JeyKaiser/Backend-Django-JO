from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers


class Referencia(models.Model):
    # Asume que U_GSP_REFERENCE es el ID/código único de la referencia que viene de SAP
    # Este campo debe coincidir con el {collectionId} en tu URL de Next.js
    codigo_referencia = models.CharField(max_length=50, unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    # Otros campos generales que describan la referencia, si los tienes

    def __str__(self):
        return f"{self.codigo_referencia} - {self.nombre}"

    # Opcional: Podrías definir una propiedad para las fases si quieres que Django las exponga
    # Esto es solo un placeholder, la lógica real de fases vendrá de SAP o configuración
    @property
    def fases_disponibles(self):
        # Esta es una simulación. En una aplicación real, aquí consultarías SAP
        # o tendrías una configuración para saber qué fases aplican a esta referencia.
        # Por ahora, devolvemos todas las fases que mencionaste.
        return [
            {"slug": "jo", "nombre": "JO"},
            {"slug": "md-creacion-ficha", "nombre": "MD CREACION FICHA"},
            {"slug": "md-creativo", "nombre": "MD CREATIVO"},
            {"slug": "md-corte", "nombre": "MD CORTE"},
            {"slug": "md-confeccion", "nombre": "MD CONFECCION"},
            {"slug": "md-fitting", "nombre": "MD FITTING"},
            {"slug": "md-tecnico", "nombre": "MD TECNICO"},
            {"slug": "md-trazador", "nombre": "MD TRAZADOR"},
            {"slug": "costeo", "nombre": "COSTEO"},
            {"slug": "pt-tecnico", "nombre": "PT TECNICO"},
            {"slug": "pt-cortador", "nombre": "PT CORTADOR"},
            {"slug": "pt-fitting", "nombre": "PT FITTING"},
            {"slug": "pt-trazador", "nombre": "PT TRAZADOR"},
        ]











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

