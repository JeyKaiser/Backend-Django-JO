from django.db import models

class Usuario(models.Model):
    """
    Modelo Usuario migrado desde el frontend DAL
    Representa la tabla GARMENT_PRODUCTION_CONTROL.T_USUARIOS
    """
    ID_USUARIO = models.AutoField(primary_key=True)
    CODIGO_USUARIO = models.CharField(max_length=50, unique=True)
    NOMBRE_COMPLETO = models.CharField(max_length=200)
    EMAIL = models.EmailField(blank=True, null=True)
    AREA = models.CharField(max_length=100)
    ROL = models.CharField(max_length=100)
    ESTADO = models.CharField(max_length=20, default='ACTIVO')
    FECHA_CREACION = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'T_USUARIOS'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['NOMBRE_COMPLETO']
    
    def __str__(self):
        return f"{self.CODIGO_USUARIO} - {self.NOMBRE_COMPLETO}"