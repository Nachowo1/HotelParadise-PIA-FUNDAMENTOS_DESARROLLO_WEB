from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class InicioSesionView(LoginView):
    template_name = "usuarios/login.html"
    redirect_authenticated_user = True


class CerrarSesionView(LogoutView):
    next_page = reverse_lazy("usuarios:login")
