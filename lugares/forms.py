from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Lugar, Resena, Lista, Etiqueta



class TimeInput(forms.TimeInput):
    input_type = "time"


class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = [
            "nombre",
            "tipo",
            "direccion",
            "comuna",
            "descripcion",   # <--- nueva
            "imagen_url",    # <--- nueva
            "horario_apertura",
            "horario_cierre",
            "wifi",
            "etiquetas",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "comuna": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows":3}),  # <--- nueva
            "imagen_url": forms.URLInput(attrs={"class": "form-control", "placeholder":"https://..."}),  # <--- nueva
            "horario_apertura": TimeInput(attrs={"class": "form-control"}),
            "horario_cierre": TimeInput(attrs={"class": "form-control"}),
            "wifi": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "etiquetas": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        apertura = cleaned.get("horario_apertura")
        cierre = cleaned.get("horario_cierre")
        if apertura and cierre and apertura == cierre:
            # opcional: advertir si son iguales (puede ser válido)
            pass
        return cleaned


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]




VALORES_CALIFICACION = [
    ("", "No aplica"),  # Se guardará como NULL en la base
    (1, "1. Muy mala"),
    (2, "2. Mala"),
    (3, "3. Regular"),
    (4, "4. Buena"),
    (5, "5. Muy buena"),
]

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["comentario", "ruido", "concurrencia", "infraestructura", "catalogo"]
        widgets = {
            "comentario": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ruido": forms.Select(choices=VALORES_CALIFICACION, attrs={"class": "form-select"}),
            "concurrencia": forms.Select(choices=VALORES_CALIFICACION, attrs={"class": "form-select"}),
            "infraestructura": forms.Select(choices=VALORES_CALIFICACION, attrs={"class": "form-select"}),
            "catalogo": forms.Select(choices=VALORES_CALIFICACION, attrs={"class": "form-select"}),
        }


class ListaForm(forms.ModelForm):
    lugares = forms.ModelMultipleChoiceField(
        queryset=Lugar.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Lista
        fields = ["nombre", "lugares"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # optional: pass request.user to filter lugares
        super().__init__(*args, **kwargs)
        if user:
            # opcional: mostrar sólo lugares que no sean borrados o filtrados
            self.fields["lugares"].queryset = Lugar.objects.all()


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }
