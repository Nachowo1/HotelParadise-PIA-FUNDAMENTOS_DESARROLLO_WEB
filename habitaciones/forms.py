from typing import ClassVar

from django import forms

from .models import Habitacion


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion

        fields = (
            "numero",
            "tipo",
            "precio_por_noche",
            "capacidad",
            "disponible",
            "imagen",
        )

        labels: ClassVar[dict] = {
            "numero": "Número de habitación",
            "tipo": "Tipo de habitación",
            "precio_por_noche": "Precio por noche",
            "capacidad": "Capacidad de personas",
            "disponible": "Disponible",
            "imagen": "Fotografía de la habitación",
        }

        widgets: ClassVar[dict] = {
            "numero": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "precio_por_noche": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "capacidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_numero(self):
        numero = self.cleaned_data["numero"]

        if numero < 1:
            raise forms.ValidationError(
                "El número de habitación debe ser mayor a cero."
            )

        return numero

    def clean_precio_por_noche(self):
        precio = self.cleaned_data["precio_por_noche"]

        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")

        return precio

    def clean_capacidad(self):
        capacidad = self.cleaned_data["capacidad"]

        if capacidad < 1:
            raise forms.ValidationError("La capacidad mínima es una persona.")

        return capacidad
