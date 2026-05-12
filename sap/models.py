from django.db import models


class SapImageAsset(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='sap/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']


class SapParametroRecord(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    base_textil = models.CharField(max_length=120)
    tela = models.CharField(max_length=120)
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    print_name = models.CharField(max_length=120)
    hilo_de_tela = models.CharField(max_length=120)
    hilo_de_molde = models.CharField(max_length=120)
    canal_tela = models.CharField(max_length=120)
    sentido_sesgos = models.CharField(max_length=120)
    rotacion_molde = models.CharField(max_length=120)
    restricciones_tela = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

