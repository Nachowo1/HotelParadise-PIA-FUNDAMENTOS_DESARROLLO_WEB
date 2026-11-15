from django.urls import path

from . import views

app_name = "habitaciones"

urlpatterns = [
    path("", views.lista_habitaciones, name="lista"),
    path("crear/", views.crear_habitacion, name="crear"),
    path("editar/<int:pk>/", views.editar_habitacion, name="editar"),
    path("eliminar/<int:pk>/", views.eliminar_habitacion, name="eliminar"),
]
