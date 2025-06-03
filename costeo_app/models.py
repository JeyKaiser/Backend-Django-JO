from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers


# Create your models here.
class Tela(models.Model):
    cod_tela = models.CharField(max_length=30, null=True, blank=True)
    descripcion_tela = models.CharField(max_length=200, null=True, blank=True)
    ancho = models.CharField(max_length=50, null=True, blank=True)
    cod_color = models.CharField(max_length=30, null=True, blank=True)
    descripcion_color = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.cod_tela

class Foto(models.Model):
    tipoFoto = models.CharField(max_length=30, null=True, blank=True)
    rutaFoto = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.tipoFoto

class Tecnico(models.Model):
    nombreTecnico = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.nombreTecnico

class Creativo(models.Model):
    nombreCreativo = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.nombreCreativo

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

class Color_Referencia(models.Model):
    codigoColor = models.CharField(max_length=200, null=True, blank=True)
    descripcionColor = models.CharField(max_length=20, null=True, blank=True)

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
    fotoReferencia = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='colecciones_foto_referencia', null=True, blank=True)
    codigoSapMD = models.CharField(max_length=30, null=True, blank=True)
    codigoSapPT = models.CharField(max_length=30, null=True, blank=True)
    nombreSistema = models.CharField(max_length=30, null=True, blank=True)
    descripcionColor = models.CharField(max_length=200, null=True, blank=True)
    codigoColor = models.CharField(max_length=20, null=True, blank=True)
    fotoTela = models.ForeignKey(Foto, on_delete=models.DO_NOTHING, related_name='colecciones_foto_tela', null=True, blank=True)
    nombreReferente = models.CharField(max_length=20, null=True, blank=True)
    linea =    models.ForeignKey(Linea, on_delete=models.DO_NOTHING, related_name='colecciones_linea', null=True, blank=True)
    creativo = models.ForeignKey(Creativo, on_delete=models.DO_NOTHING, related_name='colecciones_creativo', null=True, blank=True)
    tecnico =  models.ForeignKey(Tecnico, on_delete=models.DO_NOTHING, related_name='colecciones_tecnico', null=True, blank=True)
    status =   models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='colecciones_status', null=True, blank=True)
    tallaje =  models.CharField(max_length=50, null=True, blank=True)
    largo =    models.CharField(max_length=50, null=True, blank=True)
    modista =  models.CharField(max_length=100, null=True, blank=True)    
    def __str__(self):
        return self.referencia
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Agrega este campo

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Campos obligatorios además de USERNAME_FIELD

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

