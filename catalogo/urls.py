from django.urls import path
from . import api
from . import views

app_name = 'catalogo'

# Ojo: los ids de MongoDB son ObjectId (texto tipo '68a3...'), no enteros.
# Por eso <str:...> en vez del <int:...> que usabamos con SQLite.
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='listado'),
    path('catalogo/genero/<str:genero_id>/', views.catalogo, name='por_genero'),
    path('libro/<str:libro_id>/', views.detalle, name='detalle'),

    path('api/autores/', api.api_autores, name='api_autores'),
    path('api/generos/', api.api_generos, name='api_generos'),
    path('api/libros/', api.api_libros, name='api_libros'),
    path('api/libros/<str:libro_id>/', api.api_libro_detalle, name='api_libro_detalle'),

    path('admin-libros/', views.admin_libros, name='admin_libros'),
    path('admin-libros/nuevo/', views.admin_libro_nuevo, name='admin_libro_nuevo'),
    path('admin-libros/<str:libro_id>/editar/', views.admin_libro_editar, name='admin_libro_editar'),
    path('admin-libros/<str:libro_id>/eliminar/', views.admin_libro_eliminar, name='admin_libro_eliminar'),
]
