from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Reservacion(models.Model):
    ESTADOS = (
        ("Pendiente", "Pendiente"),
        ("Confirmada", "Confirmada"),
        ("Cancelada", "Cancelada"),
    )

    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.PROTECT, related_name="reservaciones"
    )

    habitacion = models.ForeignKey(
        "habitaciones.Habitacion",
        on_delete=models.PROTECT,
        related_name="reservaciones",
    )

    fecha_entrada = models.DateField()

    fecha_salida = models.DateField()

    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")

    def clean(self):
        super().clean()

        if not self.fecha_entrada or not self.fecha_salida:
            return

        if self.fecha_salida <= self.fecha_entrada:
            raise ValidationError(
                {"fecha_salida": "La fecha de salida debe ser posterior a la entrada."}
            )

        if (
            self.pk is None
            and self.estado != "Cancelada"
            and self.fecha_entrada < timezone.localdate()
        ):
            raise ValidationError(
                {"fecha_entrada": "No puedes crear una reservación con fecha pasada."}
            )

        if self.estado != "Cancelada" and self.habitacion_id:
            if not self.habitacion.disponible:
                raise ValidationError(
                    {
                        "habitacion": "Esta habitación no está habilitada para reservarse."
                    }
                )

            conflictos = Reservacion.objects.filter(
                habitacion_id=self.habitacion_id,
                fecha_entrada__lt=self.fecha_salida,
                fecha_salida__gt=self.fecha_entrada,
            ).exclude(estado="Cancelada")

            if self.pk:
                conflictos = conflictos.exclude(pk=self.pk)

            if conflictos.exists():
                raise ValidationError(
                    "La habitación ya está reservada durante las fechas seleccionadas."
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.habitacion_id and self.fecha_entrada and self.fecha_salida:
            noches = (self.fecha_salida - self.fecha_entrada).days

            if noches > 0:
                self.total = self.habitacion.precio_por_noche * noches

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Reservación {self.pk} - "
            f"{self.cliente} - Habitación {self.habitacion.numero}"
        )

    class Meta:
        ordering = ("-fecha_entrada",)
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"
