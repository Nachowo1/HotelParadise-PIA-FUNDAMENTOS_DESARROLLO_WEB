from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


@login_required
def inicio(request):
    hoy = timezone.localdate()

    total_clientes = Cliente.objects.count()
    total_habitaciones = Habitacion.objects.count()
    total_reservaciones = Reservacion.objects.count()

    habitaciones_ocupadas = Reservacion.objects.filter(
        estado__in=["Pendiente", "Confirmada"],
        fecha_entrada__lte=hoy,
        fecha_salida__gt=hoy,
    ).values_list("habitacion_id", flat=True)

    habitaciones_disponibles = (
        Habitacion.objects.filter(disponible=True)
        .exclude(id__in=habitaciones_ocupadas)
        .count()
    )

    ingresos = (
        Reservacion.objects.filter(estado="Confirmada").aggregate(total=Sum("total"))[
            "total"
        ]
        or 0
    )

    contexto = {
        "total_clientes": total_clientes,
        "total_habitaciones": total_habitaciones,
        "total_reservaciones": total_reservaciones,
        "habitaciones_disponibles": habitaciones_disponibles,
        "ingresos": ingresos,
    }

    return render(request, "dashboard/inicio.html", contexto)
