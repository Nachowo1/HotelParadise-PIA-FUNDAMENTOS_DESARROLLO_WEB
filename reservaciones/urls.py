from django.urls import path

from . import views

app_name = "reservaciones"

urlpatterns = [
    path("", views.lista_reservaciones, name="lista"),
    path("crear/", views.crear_reservacion, name="crear"),
    path("editar/<int:pk>/", views.editar_reservacion, name="editar"),
    path(
        "cancelar/<int:pk>/",
        views.cancelar_reservacion,
        name="cancelar",
    ),
]
