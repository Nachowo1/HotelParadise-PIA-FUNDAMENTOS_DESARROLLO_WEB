from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm
from .models import Cliente


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()

    busqueda = request.GET.get("q", "").strip()

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda)
            | Q(apellidos__icontains=busqueda)
            | Q(correo__icontains=busqueda)
        )

    contexto = {
        "clientes": clientes,
        "busqueda": busqueda,
    }

    return render(request, "clientes/lista.html", contexto)


@login_required
def crear_cliente(request):
    if request.method == "POST":
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente registrado correctamente.")
            return redirect("clientes:lista")
    else:
        formulario = ClienteForm()

    return render(
        request,
        "clientes/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar cliente",
        },
    )


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("clientes:lista")
    else:
        formulario = ClienteForm(instance=cliente)

    return render(
        request,
        "clientes/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar cliente",
        },
    )


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        try:
            cliente.delete()
            messages.success(request, "Cliente eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este cliente "
                "porque tiene reservaciones asociadas.",
            )

        return redirect("clientes:lista")

    return render(request, "clientes/confirmar_eliminar.html", {"cliente": cliente})
