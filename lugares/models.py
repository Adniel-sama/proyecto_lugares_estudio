from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


TIPO_LUGAR_CHOICES = [
    ("biblioteca", "Biblioteca"),
    ("cafe_literario", "Café literario"),
    ("cafe", "Café"),
    ("cowork", "Co-work"),
    ("otro", "Otro"),
]


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=32, choices=TIPO_LUGAR_CHOICES, db_index=True)
    direccion = models.CharField(max_length=255, blank=True)
    comuna = models.CharField(max_length=120, db_index=True)
    descripcion = models.TextField(blank=True)  # <--- nueva
    imagen_url = models.URLField(blank=True, null=True)  # <--- nueva
    horario_apertura = models.TimeField(null=True, blank=True)
    horario_cierre = models.TimeField(null=True, blank=True)
    wifi = models.BooleanField(default=False)
    agregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lugares_agregados")
    agregado_en = models.DateTimeField(auto_now_add=True, db_index=True)

    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name="lugares")

    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ["-agregado_en", "nombre"]
        indexes = [
            models.Index(fields=["tipo"]),
            models.Index(fields=["comuna"]),
            models.Index(fields=["agregado_en"]),
        ]

    def __str__(self):
        return self.nombre


class Resena(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resenas")
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="resenas")
    comentario = models.TextField(blank=True)

    ruido = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Escala 1-5 o vacío si no aplica"
    )
    concurrencia = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Escala 1-5 o vacío si no aplica"
    )
    infraestructura = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Escala 1-5 o vacío si no aplica"
    )
    catalogo = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación catálogo 1-5 o vacío si no aplica"
    )

    creado_en = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["lugar"]),
            models.Index(fields=["usuario"]),
            models.Index(fields=["creado_en"]),
        ]

    def __str__(self):
        return f"Reseña de {self.usuario} sobre {self.lugar}"



class Lista(models.Model):
    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listas")
    lugares = models.ManyToManyField(Lugar, blank=True, related_name="listas")
    creado_en = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listas"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} — {self.usuario}"


# Señal o método auxiliar (opcional) para calcular promedios:
# Puedes crear métodos en Lugar para devolver promedios calculados sobre sus reseñas,
# usando aggregation (Avg) y filtrando catalogo IS NOT NULL si corresponde.
