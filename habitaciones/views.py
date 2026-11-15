from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import HabitacionForm
from .models import Habitacion


@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()

    numero = request.GET.get("numero", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    if numero:
        habitaciones = habitaciones.filter(numero__icontains=numero)

    tipos_validos = dict(Habitacion.TIPOS_HABITACION)

    if tipo in tipos_validos:
        habitaciones = habitaciones.filter(tipo=tipo)

    contexto = {
        "habitaciones": habitaciones,
        "numero": numero,
        "tipo": tipo,
        "tipos_habitacion": Habitacion.TIPOS_HABITACION,
    }

    return render(request, "habitaciones/lista.html", contexto)


@login_required
def crear_habitacion(request):
    if request.method == "POST":
        formulario = HabitacionForm(request.POST, request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Habitación registrada correctamente.")
            return redirect("habitaciones:lista")
    else:
        formulario = HabitacionForm()

    return render(
        request,
        "habitaciones/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar habitación",
        },
    )


@login_required
def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)

    if request.method == "POST":
        formulario = HabitacionForm(request.POST, request.FILES, instance=habitacion)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Habitación actualizada correctamente.")
            return redirect("habitaciones:lista")
    else:
        formulario = HabitacionForm(instance=habitacion)

    return render(
        request,
        "habitaciones/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar habitación",
        },
    )


@login_required
def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)

    if request.method == "POST":
        try:
            habitacion.delete()
            messages.success(request, "Habitación eliminada correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar esta habitación "
                "porque tiene reservaciones asociadas.",
            )

        return redirect("habitaciones:lista")

    return render(
        request, "habitaciones/confirmar_eliminar.html", {"habitacion": habitacion}
    )
