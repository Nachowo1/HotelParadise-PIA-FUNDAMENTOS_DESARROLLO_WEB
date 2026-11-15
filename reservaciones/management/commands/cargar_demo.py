from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


class Command(BaseCommand):
    help = "Carga datos ficticios para demostrar Hotel Paradise."

    @transaction.atomic
    def handle(self, *args, **options):
        habitaciones_demo = (
            (101, "Individual", "950.00", 2),
            (102, "Doble", "1400.00", 4),
            (201, "Suite", "2500.00", 4),
            (301, "Presidencial", "5500.00", 6),
        )

        habitaciones = {}

        for numero, tipo, precio, capacidad in habitaciones_demo:
            habitacion, _ = Habitacion.objects.get_or_create(
                numero=numero,
                defaults={
                    "tipo": tipo,
                    "precio_por_noche": Decimal(precio),
                    "capacidad": capacidad,
                    "disponible": True,
                },
            )
            habitaciones[numero] = habitacion

        clientes_demo = (
            ("Ana", "García López", "ana.demo@example.com", "8111111111"),
            ("Luis", "Martínez Ruiz", "luis.demo@example.com", "8222222222"),
            ("María", "Hernández Soto", "maria.demo@example.com", "8333333333"),
        )

        clientes = {}

        for nombre, apellidos, correo, telefono in clientes_demo:
            cliente, _ = Cliente.objects.get_or_create(
                correo=correo,
                defaults={
                    "nombre": nombre,
                    "apellidos": apellidos,
                    "telefono": telefono,
                },
            )
            clientes[correo] = cliente

        hoy = timezone.localdate()

        reservas_demo = (
            (
                "ana.demo@example.com",
                101,
                hoy + timedelta(days=10),
                hoy + timedelta(days=13),
                "Confirmada",
            ),
            (
                "luis.demo@example.com",
                102,
                hoy + timedelta(days=15),
                hoy + timedelta(days=18),
                "Pendiente",
            ),
            (
                "maria.demo@example.com",
                201,
                hoy + timedelta(days=20),
                hoy + timedelta(days=22),
                "Cancelada",
            ),
        )

        for correo, numero, entrada, salida, estado in reservas_demo:
            existe = Reservacion.objects.filter(
                cliente=clientes[correo],
                habitacion=habitaciones[numero],
                fecha_entrada=entrada,
                fecha_salida=salida,
            ).exists()

            if not existe:
                Reservacion.objects.create(
                    cliente=clientes[correo],
                    habitacion=habitaciones[numero],
                    fecha_entrada=entrada,
                    fecha_salida=salida,
                    estado=estado,
                )

        self.stdout.write(
            self.style.SUCCESS("Datos de demostración cargados correctamente.")
        )
