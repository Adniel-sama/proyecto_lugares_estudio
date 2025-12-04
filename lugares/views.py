from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.urls import reverse

from .models import Lugar, Resena, Lista, Etiqueta
from .forms import LugarForm, ResenaForm, ListaForm, EtiquetaForm 


def index(request):
    return render(request, 'index.html')


# Lugares

class LugarListView(ListView):
    model = Lugar
    template_name = "lugares/lista.html"
    context_object_name = "lugares"
    paginate_by = 20


class LugarDetailView(DetailView):
    model = Lugar
    template_name = "lugares/detalle.html"
    context_object_name = "lugar"


class LugarCreateView(LoginRequiredMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = "lugares/formulario.html"
    # al crear, asignaremos agregado_por en form_valid
    success_url = reverse_lazy('lugares:list')

    def form_valid(self, form):
        form.instance.agregado_por = self.request.user
        return super().form_valid(form)


class LugarUpdateView(LoginRequiredMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = "lugares/formulario.html"
    success_url = reverse_lazy('lugares:list')

    # TODO: restringir edición solo al autor (agregado_por) si lo deseas


class LugarDeleteView(LoginRequiredMixin, DeleteView):
    model = Lugar
    template_name = "lugares/eliminar.html"
    success_url = reverse_lazy('lugares:list')

    # TODO: restringir borrado solo al autor o staff


# Reseñas

class ResenaListView(ListView):
    model = Resena
    template_name = "resenas/lista.html"
    context_object_name = "resenas"
    paginate_by = 25

    def get_queryset(self):
        """
        Si se pasa ?lugar=<pk> en la querystring, filtramos por ese lugar,
        útil para mostrar reseñas de un lugar en particular.
        """
        qs = super().get_queryset().select_related('usuario', 'lugar')
        lugar_pk = self.request.GET.get('lugar')
        if lugar_pk:
            qs = qs.filter(lugar__pk=lugar_pk)
        return qs.order_by('-creado_en')


class ResenaCreateView(LoginRequiredMixin, CreateView):
    model = Resena
    form_class = ResenaForm
    template_name = "resenas/formulario.html"

    def get_initial(self):
        initial = super().get_initial()
        lugar_pk = self.request.GET.get('lugar')
        if lugar_pk:
            initial['lugar'] = lugar_pk
        return initial

    def form_valid(self, form):
        # asignar usuario del request
        form.instance.usuario = self.request.user
        # coherencia: si marca catalogo_no_aplica dejamos catalogo=None (el modelo lo hace en save)
        return super().form_valid(form)

    def get_success_url(self):
        # redirigir al detalle del lugar si existe
        if self.object and self.object.lugar:
            return reverse('lugares:detail', args=[self.object.lugar.pk])
        return reverse_lazy('lugares:resenas')


class ResenaDetailView(DetailView):
    model = Resena
    template_name = "resenas/detalle.html"
    context_object_name = "resena"


class ResenaUpdateView(LoginRequiredMixin, UpdateView):
    model = Resena
    form_class = ResenaForm
    template_name = "resenas/formulario.html"

    def get_success_url(self):
        if self.object and self.object.lugar:
            return reverse('lugares:detail', args=[self.object.lugar.pk])
        return reverse_lazy('lugares:resenas')

    # TODO: restringir edición solo al autor (self.request.user == self.object.usuario)


class ResenaDeleteView(LoginRequiredMixin, DeleteView):
    model = Resena
    template_name = "resenas/eliminar.html"

    def get_success_url(self):
        if self.object and self.object.lugar:
            return reverse('lugares:detail', args=[self.object.lugar.pk])
        return reverse_lazy('lugares:resenas')

    # TODO: restringir borrado solo al autor o staff


# Listas (listas de lugares del usuario)

class ListaListView(ListView):
    model = Lista
    template_name = "listas/lista.html"
    context_object_name = "listas"
    paginate_by = 20

    def get_queryset(self):
        # mostrar solo listas públicas o del usuario autenticado (si implementas privacidad más adelante)
        qs = super().get_queryset().prefetch_related('lugares', 'usuario')
        if self.request.user.is_authenticated:
            # opcional: mostrar primero las propias del usuario
            return qs.order_by('-creado_en')
        return qs.order_by('-creado_en')


class ListaCreateView(LoginRequiredMixin, CreateView):
    model = Lista
    form_class = ListaForm
    template_name = "listas/formulario.html"
    success_url = reverse_lazy('lugares:listas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ListaDetailView(DetailView):
    model = Lista
    template_name = "listas/detalle.html"
    context_object_name = "lista"


class ListaUpdateView(LoginRequiredMixin, UpdateView):
    model = Lista
    form_class = ListaForm
    template_name = "listas/formulario.html"
    success_url = reverse_lazy('lugares:listas')

    # TODO: restringir edición solo al dueño (usuario)


class ListaDeleteView(LoginRequiredMixin, DeleteView):
    model = Lista
    template_name = "listas/eliminar.html"
    success_url = reverse_lazy('lugares:listas')

    # TODO: restringir borrado solo al dueño (usuario)


# Etiquetas

class EtiquetaListView(ListView):
    model = Etiqueta
    template_name = "etiquetas/lista.html"
    context_object_name = "etiquetas"


class EtiquetaCreateView(LoginRequiredMixin, CreateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = "etiquetas/formulario.html"
    success_url = reverse_lazy('lugares:etiquetas')


class EtiquetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = "etiquetas/formulario.html"
    success_url = reverse_lazy('lugares:etiquetas')
