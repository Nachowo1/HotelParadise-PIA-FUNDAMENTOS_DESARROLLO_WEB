from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from habitaciones.models import Habitacion

from .forms import ReservacionForm
from .models import Reservacion


@login_required
def lista_reservaciones(request):
    reservaciones = Reservacion.objects.select_related("cliente", "habitacion").all()

    cliente = request.GET.get("cliente", "").strip()
    habitacion = request.GET.get("habitacion", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    if cliente:
        reservaciones = reservaciones.filter(
            Q(cliente__nombre__icontains=cliente)
            | Q(cliente__apellidos__icontains=cliente)
        )

    if habitacion:
        reservaciones = reservaciones.filter(habitacion__numero__icontains=habitacion)

    tipos_validos = dict(Habitacion.TIPOS_HABITACION)

    if tipo in tipos_validos:
        reservaciones = reservaciones.filter(habitacion__tipo=tipo)

    contexto = {
        "reservaciones": reservaciones,
        "cliente": cliente,
        "habitacion": habitacion,
        "tipo": tipo,
        "tipos_habitacion": Habitacion.TIPOS_HABITACION,
    }

    return render(
        request,
        "reservaciones/lista.html",
        contexto,
    )


@login_required
def crear_reservacion(request):
    if request.method == "POST":
        formulario = ReservacionForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Reservación registrada correctamente.")
            return redirect("reservaciones:lista")
    else:
        formulario = ReservacionForm()

    return render(
        request,
        "reservaciones/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar reservación",
        },
    )


@login_required
def editar_reservacion(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)

    if request.method == "POST":
        formulario = ReservacionForm(
            request.POST,
            instance=reservacion,
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Reservación actualizada correctamente.")
            return redirect("reservaciones:lista")
    else:
        formulario = ReservacionForm(instance=reservacion)

    return render(
        request,
        "reservaciones/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar reservación",
        },
    )


@login_required
def cancelar_reservacion(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)

    if request.method == "POST":
        if reservacion.estado == "Cancelada":
            messages.warning(request, "Esta reservación ya estaba cancelada.")
        else:
            reservacion.estado = "Cancelada"
            reservacion.save(update_fields=["estado"])

            messages.success(request, "Reservación cancelada correctamente.")

        return redirect("reservaciones:lista")

    return render(
        request,
        "reservaciones/confirmar_cancelar.html",
        {"reservacion": reservacion},
    )
