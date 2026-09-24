"""
Acceso a datos del catálogo.

Responsabilidad única de este archivo: hablar con la base de datos.
Es el ÚNICO archivo que importa mongoengine o catalogo/documents.py.

Si algún día cambiamos de base de datos (por ejemplo, volver a SQLite
o pasar a PostgreSQL), este es el único archivo que hay que reescribir.
Las vistas, los formularios y los templates no saben que existe Mongo:
solo llaman a estas funciones y reciben objetos Libro/Genero/Autor de
vuelta, o la excepción NoEncontrado.
"""

from mongoengine.errors import DoesNotExist
from mongoengine.errors import ValidationError as ValidacionMongo

from .documents import Autor, Genero, Libro


class NoEncontrado(Exception):
    """Se buscó un documento (libro, género o autor) que no existe."""


class DatosInvalidos(Exception):
    """El libro no pasó las validaciones del esquema al guardarlo."""


# ---------- Géneros ----------

def listar_generos():
    return list(Genero.objects().order_by('nombre'))


def obtener_genero(genero_id):
    try:
        return Genero.objects.get(pk=genero_id)
    except (DoesNotExist, ValidacionMongo):
        raise NoEncontrado(f'No existe un género con id {genero_id}')


def listar_generos_con_conteo():
    """Cada género con cuántos libros tiene (no hay JOIN en Mongo, se cuenta a mano)."""
    generos = listar_generos()

    conteos = {}
    for libro in Libro.objects().only('genero'):
        gid = libro.genero.id
        conteos[gid] = conteos.get(gid, 0) + 1

    for genero in generos:
        genero.total_libros = conteos.get(genero.id, 0)

    return generos


# ---------- Autores ----------

def listar_autores():
    return list(Autor.objects().order_by('nombre'))


def obtener_autor(autor_id):
    try:
        return Autor.objects.get(pk=autor_id)
    except (DoesNotExist, ValidacionMongo):
        raise NoEncontrado(f'No existe un autor con id {autor_id}')


# ---------- Libros ----------

def contar_libros():
    return Libro.objects().count()


def listar_libros(genero=None):
    libros = Libro.objects(genero=genero) if genero else Libro.objects()
    return libros.order_by('titulo')


def obtener_libro(libro_id):
    try:
        return Libro.objects.get(pk=libro_id)
    except (DoesNotExist, ValidacionMongo):
        raise NoEncontrado(f'No existe un libro con id {libro_id}')


def libros_relacionados(libro, limite=4):
    return Libro.objects(genero=libro.genero).filter(pk__ne=libro.pk)[:limite]


def libro_nuevo():
    """Instancia vacía, todavía sin guardar en la base de datos."""
    return Libro()


def guardar_libro(libro, titulo, autor, genero, anio, stock, sinopsis, imagen=''):
    """Rellena el libro (nuevo o existente) y lo guarda."""
    libro.titulo = titulo
    libro.autor = autor
    libro.genero = genero
    libro.anio = anio
    libro.stock = stock
    libro.sinopsis = sinopsis
    libro.imagen = imagen

    try:
        libro.save()
    except ValidacionMongo as e:
        raise DatosInvalidos(str(e))

    return libro


def eliminar_libro(libro):
    libro.delete()
