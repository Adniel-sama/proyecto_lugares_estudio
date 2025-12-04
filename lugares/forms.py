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


class ResenaForm(forms.ModelForm):
    ruido = forms.ChoiceField(
        choices=[("", "—")] + RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Ruido (1-5)",
    )
    concurrencia = forms.ChoiceField(
        choices=[("", "—")] + RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Concurrencia (1-5)",
    )
    infraestructura = forms.ChoiceField(
        choices=[("", "—")] + RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Infraestructura (1-5)",
    )

    catalogo = forms.ChoiceField(
        choices=[("", "—")] + RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Catálogo (1-5)",
    )
    catalogo_no_aplica = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Catálogo no aplica",
    )

    class Meta:
        model = Resena
        fields = ["lugar", "comentario", "ruido", "concurrencia", "infraestructura", "catalogo", "catalogo_no_aplica"]
        widgets = {
            "lugar": forms.HiddenInput(),  # normalmente pasamos lugar por querystring o hidden field
            "comentario": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()

        no_aplica = cleaned.get("catalogo_no_aplica")
        catalogo = cleaned.get("catalogo")

        # Normalize empty strings to None (because we use ChoiceField)
        if catalogo == "":
            catalogo = None
            cleaned["catalogo"] = None

        if no_aplica and catalogo is not None:
            raise ValidationError(_("Si marca 'Catálogo no aplica', el campo 'Catálogo' debe estar vacío."))
        return cleaned

    def save(self, commit=True):
        # Convert choice strings to int or None before saving to model
        instance = super().save(commit=False)
        cat = self.cleaned_data.get("catalogo")
        if cat in (None, ""):
            instance.catalogo = None
        else:
            instance.catalogo = int(cat)
        instance.catalogo_no_aplica = bool(self.cleaned_data.get("catalogo_no_aplica", False))

        # For other rating fields (they come as strings), convert to int or None
        for field in ("ruido", "concurrencia", "infraestructura"):
            val = self.cleaned_data.get(field)
            setattr(instance, field, int(val) if val not in (None, "") else None)

        if commit:
            instance.save()
            # If there are M2M (none here), call save_m2m in the CreateView's form_valid via form.save_m2m()
        return instance


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
