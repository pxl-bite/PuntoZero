from django.db import models
from django.contrib.auth.models import User

class Solicitud(models.Model):
    TIPO_TRAMITE_CHOICES = [
        ('vehicular', 'Vehicular'),
        ('sat', 'SAT'),
        ('acta', 'Acta de nacimiento'),
        ('antecedentes', 'Antecedentes no penales'),
        ('nss', 'Número de seguridad social'),
        ('vigencia', 'Vigencia de derechos'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    tipo_tramite = models.CharField(
        max_length=20,
        choices=TIPO_TRAMITE_CHOICES
    )

    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    curp = models.CharField(max_length=18)
    correo = models.EmailField()
    whatsapp = models.CharField(max_length=15)

    datos_extra = models.TextField(blank=True)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_tramite} - {self.nombre}"
