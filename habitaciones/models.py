from django.db import models


class Habitacion(models.Model):
    TIPOS_HABITACION = (
        ("Individual", "Individual"),
        ("Doble", "Doble"),
        ("Suite", "Suite"),
        ("Presidencial", "Presidencial"),
    )

    numero = models.PositiveIntegerField(unique=True)

    tipo = models.CharField(max_length=20, choices=TIPOS_HABITACION)

    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)

    capacidad = models.PositiveIntegerField()

    disponible = models.BooleanField(default=True)

    imagen = models.ImageField(upload_to="habitaciones/", blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"

    class Meta:
        ordering = ("numero",)
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
