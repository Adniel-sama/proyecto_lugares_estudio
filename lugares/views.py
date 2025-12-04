from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy, reverse

from .models import Lugar, Resena, Lista, Etiqueta
from .forms import LugarForm, ResenaForm, ListaForm, EtiquetaForm

from django.contrib import messages

from django.http import HttpResponseForbidden



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
    # No namespace: usamos el nombre de url sin prefijo
    success_url = reverse_lazy('lista_lugares')

    def form_valid(self, form):
        form.instance.agregado_por = self.request.user
        return super().form_valid(form)


class LugarUpdateView(LoginRequiredMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = "lugares/formulario.html"
    success_url = reverse_lazy('lista_lugares')


class LugarDeleteView(LoginRequiredMixin, DeleteView):
    model = Lugar
    template_name = "lugares/eliminar.html"
    success_url = reverse_lazy('lista_lugares')


# Reseñas

class ResenaListView(ListView):
    model = Resena
    template_name = "resenas/lista.html"
    context_object_name = "resenas"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related('usuario', 'lugar')
        lugar_pk = self.request.GET.get('lugar')
        if lugar_pk:
            qs = qs.filter(lugar__pk=lugar_pk)
        return qs.order_by('-creado_en')





from django.contrib import messages
from django.urls import reverse, reverse_lazy

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lugar_pk = self.request.GET.get('lugar') or self.get_initial().get('lugar')
        if lugar_pk:
            try:
                ctx['cancel_url'] = reverse('detalle_lugar', args=[lugar_pk])
            except Exception:
                ctx['cancel_url'] = reverse_lazy('lista_resenas')
        else:
            ctx['cancel_url'] = reverse_lazy('lista_resenas')
        return ctx

    def dispatch(self, request, *args, **kwargs):
        """
        Solo permitir crear reseñas si viene ?lugar=PK (es decir, desde la página del lugar).
        Si no viene, redirigimos a la lista de reseñas.
        """
        lugar_pk = request.GET.get('lugar') or (self.get_initial().get('lugar') if hasattr(self, 'get_initial') else None)
        if not lugar_pk:
            messages.warning(request, "Las reseñas solo se pueden crear desde la página de un lugar.")
            return redirect('lista_resenas')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # asignar usuario
        form.instance.usuario = self.request.user

        # lugar puede venir como instancia (ModelChoiceField) o como pk (string)
        lugar_val = form.cleaned_data.get('lugar') or self.request.GET.get('lugar')

        # si es instancia de Lugar, usar directamente
        if isinstance(lugar_val, Lugar):
            form.instance.lugar = lugar_val
        else:
            # intentar convertir/obtener por pk
            try:
                lugar_obj = Lugar.objects.get(pk=int(lugar_val))
                form.instance.lugar = lugar_obj
            except (TypeError, ValueError, Lugar.DoesNotExist):
                form.add_error('lugar', 'Lugar no válido.')
                return self.form_invalid(form)

        response = super().form_valid(form)
        try:
            form.save_m2m()
        except Exception:
            pass

        messages.success(self.request, "Reseña guardada correctamente.")
        return response

    def get_success_url(self):
        if self.object and self.object.lugar:
            return reverse('detalle_lugar', args=[self.object.lugar.pk])
        return reverse_lazy('lista_resenas')



class ResenaDetailView(DetailView):
    model = Resena
    template_name = "resenas/detalle.html"
    context_object_name = "resena"




class ResenaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resena
    form_class = ResenaForm
    template_name = "resenas/formulario.html"

    def test_func(self):
        # solo el autor puede editar
        resena = self.get_object()
        return self.request.user == resena.usuario

    def handle_no_permission(self):
        # devuelve 403 (puedes redirigir en su lugar si prefieres)
        return HttpResponseForbidden("No tienes permiso para editar esta reseña.")

    def get_success_url(self):
        if self.object and self.object.lugar:
            return reverse('detalle_lugar', args=[self.object.lugar.pk])
        return reverse_lazy('lista_resenas')


class ResenaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resena
    template_name = "resenas/eliminar.html"

    def test_func(self):
        resena = self.get_object()
        return self.request.user == resena.usuario

    def handle_no_permission(self):
        return HttpResponseForbidden("No tienes permiso para eliminar esta reseña.")

    def get_success_url(self):
        if self.object and self.object.lugar:
            return reverse('detalle_lugar', args=[self.object.lugar.pk])
        return reverse_lazy('lista_resenas')



# Listas

class ListaListView(ListView):
    model = Lista
    template_name = "listas/lista.html"
    context_object_name = "listas"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('lugares', 'usuario')
        return qs.order_by('-creado_en')


class ListaCreateView(LoginRequiredMixin, CreateView):
    model = Lista
    form_class = ListaForm
    template_name = "listas/formulario.html"
    success_url = reverse_lazy('lista_listas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ListaDetailView(DetailView):
    model = Lista
    template_name = "listas/detalle.html"
    context_object_name = "lista"


class ListaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lista
    form_class = ListaForm
    template_name = "listas/formulario.html"
    success_url = reverse_lazy('lista_listas')

    def test_func(self):
        lista = self.get_object()
        return self.request.user == lista.usuario

    def handle_no_permission(self):
        return HttpResponseForbidden("No tienes permiso para editar esta lista.")


class ListaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lista
    template_name = "listas/eliminar.html"
    success_url = reverse_lazy('lista_listas')

    def test_func(self):
        lista = self.get_object()
        return self.request.user == lista.usuario

    def handle_no_permission(self):
        return HttpResponseForbidden("No tienes permiso para eliminar esta lista.")



# Etiquetas

class EtiquetaListView(ListView):
    model = Etiqueta
    template_name = "etiquetas/lista.html"
    context_object_name = "etiquetas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        etiqueta_nombre = self.request.GET.get('etiqueta')
        if etiqueta_nombre:
            context['lugares'] = Lugar.objects.filter(etiquetas__nombre=etiqueta_nombre)
        else:
            context['lugares'] = []
        return context


class EtiquetaCreateView(LoginRequiredMixin, CreateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = "etiquetas/formulario.html"
    success_url = reverse_lazy('lista_etiquetas')


class EtiquetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = "etiquetas/formulario.html"
    success_url = reverse_lazy('lista_etiquetas')
