from django.urls import path

from .views import CerrarSesionView, InicioSesionView

app_name = "usuarios"

urlpatterns = [
    path("login/", InicioSesionView.as_view(), name="login"),
    path("logout/", CerrarSesionView.as_view(), name="logout"),
]
