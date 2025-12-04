# Proyecto Lugares de Estudio

Este proyecto es una aplicación web desarrollada con Django 6 que permite a los usuarios gestionar y explorar lugares de estudio, crear listas personalizadas y escribir reseñas sobre los lugares que visitan. 

## Funcionalidades principales

- Registro, inicio y cierre de sesión de usuarios mediante el sistema de autenticación de Django.
- Visualización de lugares de estudio con detalle de cada uno.
- Creación, edición y eliminación de listas de lugares personales (favoritos, pendientes, etc.), asociadas al usuario que las crea.
- Creación, edición y eliminación de reseñas asociadas a cada lugar. Solo el autor puede modificarlas.
- Gestión de etiquetas y categorización de lugares para facilitar búsquedas.
- Uso de vistas basadas en clases (ListView, DetailView, CreateView, UpdateView, DeleteView) y formularios personalizados con Django Forms.
- Plantillas organizadas con un layout base (`base.html`) y subcarpetas para cada modelo (`lugares/`, `listas/`, `resenas/`, etc.).
- Conexión a base de datos MySQL para almacenamiento de usuarios, lugares, listas, reseñas y etiquetas.

## Estructura del proyecto
- `usuarios/` — aplicación básica prediseñada con las funcionalidades propias de django
- `lugares/` — aplicación principal con modelos, vistas y templates.
- `templates/` — plantillas HTML organizadas por modelos.
- `urls.py` — enrutamiento principal y de la app `lugares`.
- `forms.py` — formularios personalizados para creación y edición de modelos.
- `views.py` — vistas basadas en clases y funciones para CRUD y página de inicio.
- `settings.py` — configuración de base de datos, aplicaciones instaladas, rutas de templates y autenticación.


## Ejecución

1. Crear y activar un entorno virtual.
2. Instalar dependencias
3. Configurar la base de datos en `settings.py`.
4. Ejecutar migraciones: `python manage.py migrate`.
5. Crear superusuario (opcional): `python manage.py createsuperuser`.
6. Ejecutar servidor de desarrollo: `python manage.py runserver`.
7. Acceder a la aplicación en `http://127.0.0.1:8000/`.

