from typing import ClassVar

from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        fields = (
            "nombre",
            "apellidos",
            "correo",
            "telefono",
        )

        labels: ClassVar[dict] = {
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "correo": "Correo electrónico",
            "telefono": "Teléfono",
        }

        widgets: ClassVar[dict] = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_correo(self):
        correo = self.cleaned_data["correo"]
        return correo.strip().lower()
