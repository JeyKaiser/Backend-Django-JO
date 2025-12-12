from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers


# Create your models here.
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
    is_superuser = models.BooleanField(default=False)  

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Campos obligatorios además de USERNAME_FIELD

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class TUsuarios(models.Model):
    """
    Modelo para la tabla T_USUARIOS en SAP HANA
    Compatible con el frontend Next.js
    """
    
    # Campos principales
    codigo_usuario = models.CharField(max_length=50, unique=True, verbose_name="Código de Usuario")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Área/Departamento")
    
    # Rol con opciones predefinidas
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('USER', 'Usuario'),
        ('MANAGER', 'Gerente'),
        ('SUPERVISOR', 'Supervisor'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='USER', verbose_name="Rol")
    
    # Estado con opciones predefinidas
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    ultimo_acceso = models.DateTimeField(blank=True, null=True, verbose_name="Último Acceso")

    class Meta:
        db_table = 'GARMENT_PRODUCTION_CONTROL.T_USUARIOS'
        verbose_name = "Usuario SAP HANA"
        verbose_name_plural = "Usuarios SAP HANA"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.codigo_usuario} - {self.nombres} {self.apellidos}"
    
    @property
    def full_name(self):
        return f"{self.nombres} {self.apellidos}".strip()
    
    def to_frontend_format(self):
        """
        Convierte el modelo al formato esperado por el frontend Next.js
        """
        return {
            'id': str(self.id),
            'firstName': self.nombres,
            'lastName': self.apellidos,
            'email': self.email,
            'role': self.rol,
            'status': self.estado,
            'phone': self.telefono,
            'department': self.area,
            'joinedAt': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'lastLoginAt': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
        }

