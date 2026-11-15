from typing import ClassVar

from django import forms

from .models import Reservacion


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion

        fields = (
            "cliente",
            "habitacion",
            "fecha_entrada",
            "fecha_salida",
            "estado",
        )

        labels: ClassVar[dict] = {
            "cliente": "Cliente",
            "habitacion": "Habitación",
            "fecha_entrada": "Fecha de entrada",
            "fecha_salida": "Fecha de salida",
            "estado": "Estado de la reservación",
        }

        widgets: ClassVar[dict] = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "habitacion": forms.Select(attrs={"class": "form-select"}),
            "fecha_entrada": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "fecha_salida": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
