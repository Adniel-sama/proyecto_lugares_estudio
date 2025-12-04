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


# Proyecto Lugares de Estudio
![[1.png]](capturas/1.png)
## Descripción
Este proyecto es una aplicación web para gestionar y explorar "lugares de estudio". Permite a los usuarios registrar lugares, añadir reseñas, asignar calificaciones y etiquetar los espacios según sus características, con el objetivo de que se puedan compartir experiencias e información, de manera que se puedan encontrar los lugares más adecuados para cada persona.
Los usuarios pueden visualizar información detallada, filtrar por etiquetas (para lo cual tienen total libertad, quizá demasiada) y ver estadísticas agregadas de calificaciones.
![[6.png]](capturas/6.png)
Manualmente se pueden agregar hashtags de lo que sea, en las pruebas se usó #opciónvegan o #petfriendly, pero otras como #bicicletero para los ciclistas también puede ser una buena idea. 

## Funcionalidades principales
![[2.png]](capturas/3.png)
- 
- Registro y autenticación de usuarios mediante las herramientas de Django.
- Gestión de lugares: creación, edición y eliminación.
- Gestión de reseñas: los usuarios pueden calificar lugares en varios aspectos (ruido, concurrencia, infraestructura, catálogo) y agregar comentarios.
- Sistema de etiquetas: permite clasificar los lugares y filtrar la visualización.
- Visualización de estadísticas: promedio por cada aspecto y promedio general de calificaciones de los lugares.
- Interfaz amigable usando Bootstrap con diseño responsivo y plantillas en español.
![[4.png]](capturas/4.png)
## Proceso de desarrollo
1. Configuración del proyecto Django con aplicaciones `usuarios`, que fue tomada de lo que vimos en clases y que se basa en las herramientas propias de django.  Y la app `lugares`, que contiene el grueso de los modelos, tablas y funcionalidades.
2. Creación de modelos para `Lugar`, `Reseña` y `Etiqueta` con relaciones adecuadas.
3. Desarrollo de vistas usando `Class-Based Views` para CRUD de lugares, reseñas y etiquetas.
4. Implementación de formularios personalizados y validaciones, incluyendo escalas de calificación 1–5 y control de permisos según el usuario creador.
5. Diseño de templates en subcarpetas (`lugares/`, `resenas/`, `etiquetas/`) y plantilla base `base.html` con navbar y footer comunes.
6. Generación de estadísticas y promedios usando SQL crudo para ignorar valores nulos en las calificaciones.
7. Iteración sobre detalles de UI: visualización de imágenes, manejo de etiquetas y control de botones según permisos.
![[5.png]](capturas/5.png)
## Retos encontrados y soluciones
- **Gestión de permisos:** se implementó lógica para que solo el creador pueda editar o eliminar reseñas, listas y lugares, a veces puede ser un poco tedioso el configurar quién puede ver qué, y cómo pequeños errores pueden generar problemas.
- **Cálculo de promedios ignorando nulos:** se resolvió mediante consultas SQL con `AVG()` y `CASE WHEN` para calcular el promedio general correctamente.  Se eligió trabajar con `Nulls` porque si se tomaran como 0, pueden sesgar los resultados, en un proyecto con fines educativos quizás no es tan relevante, pero en el mundo real, si se trabaja con datos reales de interés, sería un error imperdonable.
![[7.png]](capturas/7.png)

- La gran cantidad de plantillas y páginas, puede ser un poco engorrosa, y confuso al generar las URLs y sus configuraciones, se usó subcarpetas para intentar mantener un poco de orden.
- **Vinculación de reseñas a lugares:** se ajustó la lógica de creación para asociar automáticamente la reseña al lugar seleccionado.  
- **Formulario de edición y creación:** se solucionó el problema de precarga de datos en la edición y la correcta persistencia en la base de datos.  
- **Interfaz responsiva:** se aplicó Bootstrap y estilos CSS para un diseño consistente y accesible.
- La sugerencia de agregar imágenes a la base de datos, fue solucionado de una manera sencilla y eficiente, pero poco recomendable: el uso de enlaces externos y su guardado como cadena de texto.
- La responsividad, fue trabajo de bootstrap. 











![[3.png]](capturas/3.png)

## Tecnologías usadas
- Python 3.x
- Django 6
- Bootstrap 5
- MySQL / SQLite
- HTML5, CSS3, Django Templates

## Conclusión
El proyecto permitió consolidar conocimientos en desarrollo web con Django, manejo de bases de datos, control de permisos y creación de interfaces dinámicas. Los retos surgidos durante el desarrollo reforzaron la capacidad de resolver problemas prácticos y de optimizar consultas y lógica de negocio.
