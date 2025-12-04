from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    # Lugares
    path('lista/', LugarListView.as_view(), name='lista_lugares'),
    path('crear/', LugarCreateView.as_view(), name='crear_lugar'),
    path('<int:pk>/', LugarDetailView.as_view(), name='detalle_lugar'),
    path('<int:pk>/editar/', LugarUpdateView.as_view(), name='editar_lugar'),
    path('<int:pk>/eliminar/', LugarDeleteView.as_view(), name='eliminar_lugar'),

    # Reseñas
    path('resenas/', ResenaListView.as_view(), name='lista_resenas'),
    path('resenas/crear/', ResenaCreateView.as_view(), name='crear_resena'),
    path('resenas/<int:pk>/', ResenaDetailView.as_view(), name='detalle_resena'),
    path('resenas/<int:pk>/editar/', ResenaUpdateView.as_view(), name='editar_resena'),
    path('resenas/<int:pk>/eliminar/', ResenaDeleteView.as_view(), name='eliminar_resena'),

    # Listas
    path('listas/', ListaListView.as_view(), name='lista_listas'),
    path('listas/crear/', ListaCreateView.as_view(), name='crear_lista'),
    path('listas/<int:pk>/', ListaDetailView.as_view(), name='detalle_lista'),
    path('listas/<int:pk>/editar/', ListaUpdateView.as_view(), name='editar_lista'),
    path('listas/<int:pk>/eliminar/', ListaDeleteView.as_view(), name='eliminar_lista'),

    # Etiquetas
    path('etiquetas/', EtiquetaListView.as_view(), name='lista_etiquetas'),
    path('etiquetas/crear/', EtiquetaCreateView.as_view(), name='crear_etiqueta'),
    path('etiquetas/<int:pk>/editar/', EtiquetaUpdateView.as_view(), name='editar_etiqueta'),
]
