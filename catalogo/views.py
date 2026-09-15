"""
Vistas del catálogo.

Responsabilidad única de este archivo: traducir peticiones HTTP en
llamadas a repositorios.py (datos) y formularios.py (validación), y
elegir qué template mostrar. Ninguna vista sabe que la base de datos es
MongoDB — eso vive solo en repositorios.py.
"""

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import formularios, repositorios


def inicio(request):
    """Página inicial: los géneros que existen, con su conteo de libros."""
    generos = sorted(
        repositorios.listar_generos_con_conteo(),
        key=lambda g: (-g.total_libros, g.nombre),
    )
    return render(request, 'catalogo/inicio.html', {
        'generos': generos,
        'total_libros': repositorios.contar_libros(),
    })


def catalogo(request, genero_id=None):
    """Catálogo de libros. Si viene un género en la URL, filtra por ese género."""
    genero = None

    if genero_id is not None:
        try:
            genero = repositorios.obtener_genero(genero_id)
        except repositorios.NoEncontrado:
            raise Http404('Género no encontrado')

    return render(request, 'catalogo/listado.html', {
        'libros': repositorios.listar_libros(genero=genero),
        'genero': genero,
        'generos': repositorios.listar_generos_con_conteo(),
    })


def detalle(request, libro_id):
    try:
        libro = repositorios.obtener_libro(libro_id)
    except repositorios.NoEncontrado:
        raise Http404('Libro no encontrado')

    return render(request, 'catalogo/detalle.html', {
        'libro': libro,
        'relacionados': repositorios.libros_relacionados(libro),
    })


# ---------------------------------------------------------------------------
# Admin (CRUD de libros)
# ---------------------------------------------------------------------------

def admin_libros(request):
    """Tabla dinámica con todos los libros."""
    return render(request, 'catalogo/admin_lista.html', {
        'libros': repositorios.listar_libros(),
    })


def admin_libro_nuevo(request):
    datos_formulario = {}

    if request.method == 'POST':
        limpios, errores = formularios.limpiar_libro(request.POST)
        if not errores:
            libro = repositorios.guardar_libro(repositorios.libro_nuevo(), **limpios)
            messages.success(request, f'Libro "{libro.titulo}" creado.')
            return redirect('catalogo:admin_libros')
        for error in errores:
            messages.error(request, error)
        datos_formulario = request.POST

    return render(request, 'catalogo/admin_form.html', {
        'accion': 'Crear',
        'libro': datos_formulario,
        'autor_id': datos_formulario.get('autor', ''),
        'genero_id': datos_formulario.get('genero', ''),
        'autores': repositorios.listar_autores(),
        'generos': repositorios.listar_generos(),
    })


def admin_libro_editar(request, libro_id):
    try:
        libro = repositorios.obtener_libro(libro_id)
    except repositorios.NoEncontrado:
        raise Http404('Libro no encontrado')

    datos_formulario = libro
    autor_id, genero_id = str(libro.autor.id), str(libro.genero.id)

    if request.method == 'POST':
        limpios, errores = formularios.limpiar_libro(request.POST)
        if not errores:
            libro = repositorios.guardar_libro(libro, **limpios)
            messages.success(request, f'Libro "{libro.titulo}" actualizado.')
            return redirect('catalogo:admin_libros')
        for error in errores:
            messages.error(request, error)
        datos_formulario = request.POST
        autor_id = datos_formulario.get('autor', '')
        genero_id = datos_formulario.get('genero', '')

    return render(request, 'catalogo/admin_form.html', {
        'accion': 'Editar',
        'libro': datos_formulario,
        'autor_id': autor_id,
        'genero_id': genero_id,
        'autores': repositorios.listar_autores(),
        'generos': repositorios.listar_generos(),
    })


def admin_libro_eliminar(request, libro_id):
    try:
        libro = repositorios.obtener_libro(libro_id)
    except repositorios.NoEncontrado:
        raise Http404('Libro no encontrado')

    if request.method == 'POST':
        titulo = libro.titulo
        repositorios.eliminar_libro(libro)
        messages.success(request, f'Libro "{titulo}" eliminado.')

    return redirect('catalogo:admin_libros')
