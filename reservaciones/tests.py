from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion

from .models import Reservacion


class ReservacionTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Carlos",
            apellidos="Martínez López",
            correo="pruebas@example.com",
            telefono="8112345678",
        )

        self.habitacion = Habitacion.objects.create(
            numero=101,
            tipo="Individual",
            precio_por_noche=Decimal("950.00"),
            capacidad=2,
            disponible=True,
        )

        self.entrada = timezone.localdate() + timedelta(days=10)
        self.salida = self.entrada + timedelta(days=5)

    def crear_reservacion(self):
        return Reservacion.objects.create(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=self.entrada,
            fecha_salida=self.salida,
            estado="Confirmada",
        )

    def test_reservacion_valida(self):
        reservacion = self.crear_reservacion()

        self.assertEqual(
            reservacion.total,
            Decimal("4750.00"),
        )

    def test_fechas_invalidas(self):
        reservacion = Reservacion(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=self.salida,
            fecha_salida=self.entrada,
        )

        with self.assertRaises(ValidationError):
            reservacion.full_clean()

    def test_fechas_superpuestas(self):
        self.crear_reservacion()

        segunda = Reservacion(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=self.entrada + timedelta(days=2),
            fecha_salida=self.salida + timedelta(days=2),
        )

        with self.assertRaises(ValidationError):
            segunda.full_clean()

    def test_fechas_consecutivas(self):
        self.crear_reservacion()

        segunda = Reservacion.objects.create(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=self.salida,
            fecha_salida=self.salida + timedelta(days=3),
        )

        self.assertIsNotNone(segunda.pk)

    def test_cancelacion_libera_fechas(self):
        primera = self.crear_reservacion()

        primera.estado = "Cancelada"
        primera.save()

        segunda = Reservacion.objects.create(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=self.entrada,
            fecha_salida=self.salida,
        )

        self.assertIsNotNone(segunda.pk)

    def test_cancelar_reservacion_historica(self):
        entrada = timezone.localdate() - timedelta(days=10)
        salida = entrada + timedelta(days=3)

        reservacion = Reservacion(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=entrada,
            fecha_salida=salida,
            estado="Confirmada",
        )

        # Simulamos una reservación histórica existente.
        Reservacion.objects.bulk_create([reservacion])

        historica = Reservacion.objects.get(habitacion=self.habitacion)

        historica.estado = "Cancelada"
        historica.save(update_fields=["estado"])

        historica.refresh_from_db()

        self.assertEqual(historica.estado, "Cancelada")

    def test_no_eliminar_habitacion_con_reservacion(self):
        self.crear_reservacion()

        with self.assertRaises(ProtectedError):
            self.habitacion.delete()

        self.assertTrue(Habitacion.objects.filter(pk=self.habitacion.pk).exists())
