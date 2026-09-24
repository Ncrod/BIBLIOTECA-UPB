"""
Agrega la portada (URL) a los libros de Mongo y crea libros nuevos con foto.

Uso:
    python manage.py poblar_portadas

Las portadas salen de Open Library (covers.openlibrary.org). Se puede correr
varias veces: solo busca portada de los libros que aun no tienen, y no
duplica los libros nuevos.
"""

import json
import re
import unicodedata
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand

from catalogo import documents as mongo

# (titulo, autor, genero, anio, stock, sinopsis)
LIBROS_NUEVOS = [
    ('Frankenstein', 'Mary Shelley', 'Clásicos', 1818, 4,
     'Un científico crea vida y no sabe qué hacer con ella.'),
    ('Drácula', 'Bram Stoker', 'Clásicos', 1897, 3,
     'Cartas y diarios contra el conde de Transilvania.'),
    ('El principito', 'Antoine de Saint-Exupéry', 'Clásicos', 1943, 7,
     'Un niño de otro planeta enseña a mirar lo esencial.'),
    ('Fahrenheit 451', 'Ray Bradbury', 'Distopía', 1953, 5,
     'Bomberos que queman libros en vez de apagar incendios.'),
    ('Neuromante', 'William Gibson', 'Ciencia Ficción', 1984, 2,
     'Hackers, inteligencias artificiales y ciberespacio.'),
    ('Crónica de una muerte anunciada', 'Gabriel García Márquez', 'Realismo mágico', 1981, 6,
     'Todo el pueblo sabía que iban a matar a Santiago Nasar.'),
    ('Los juegos del hambre', 'Suzanne Collins', 'Distopía', 2008, 9,
     'Un torneo a muerte transmitido por televisión.'),
    ('El nombre del viento', 'Patrick Rothfuss', 'Fantasía', 2007, 4,
     'La historia de Kvothe contada por él mismo.'),
]


# Open Library indexa por titulo original; estos no aparecen con el titulo en español.
TITULOS_EN = {
    'El nombre del viento': 'The Name of the Wind',
    'Harry Potter y la piedra filosofal': "Harry Potter and the Philosopher's Stone",
    'La mano izquierda de la oscuridad': 'The Left Hand of Darkness',
    'Los juegos del hambre': 'The Hunger Games',
    'Neuromante': 'Neuromancer',
    'Yo, robot': 'I, Robot',
}


def correo_de(nombre):
    """Apellido en ascii minusculas, valido para un correo."""
    ascii_ = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', ascii_.split()[-1].lower())


def buscar_portada(titulo, autor):
    """URL de la portada en Open Library, o '' si no la encuentra."""
    params = urllib.parse.urlencode({
        'title': titulo, 'author': autor, 'fields': 'cover_i', 'limit': 5,
    })
    try:
        with urllib.request.urlopen(
            f'https://openlibrary.org/search.json?{params}', timeout=20
        ) as resp:
            docs = json.load(resp).get('docs', [])
    except Exception:
        return ''

    for doc in docs:
        if doc.get('cover_i'):
            return f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    return ''


class Command(BaseCommand):
    help = 'Agrega portadas a los libros y crea libros nuevos con foto.'

    def handle(self, *args, **options):
        # 1. Libros nuevos (y sus autores/generos si faltan).
        creados = 0
        for titulo, autor, genero, anio, stock, sinopsis in LIBROS_NUEVOS:
            if mongo.Libro.objects(titulo=titulo).first():
                continue
            doc_autor = mongo.Autor.objects(nombre=autor).first() or mongo.Autor(
                nombre=autor,
                contacto=f'{correo_de(autor)}@editorial.com',
            ).save()
            doc_genero = mongo.Genero.objects(nombre=genero).first() or mongo.Genero(
                nombre=genero,
            ).save()
            mongo.Libro(
                titulo=titulo, autor=doc_autor, genero=doc_genero,
                anio=anio, stock=stock, sinopsis=sinopsis,
            ).save()
            creados += 1

        # 2. Portada para todo libro que no tenga.
        con_foto = sin_foto = 0
        for libro in mongo.Libro.objects():
            if libro.imagen:
                continue
            url = buscar_portada(TITULOS_EN.get(libro.titulo, libro.titulo), libro.autor.nombre)
            if url:
                libro.imagen = url
                libro.save()
                con_foto += 1
            else:
                sin_foto += 1
                self.stdout.write(self.style.WARNING(f'Sin portada: {libro.titulo}'))

        self.stdout.write(self.style.SUCCESS(
            f'Libros nuevos: {creados}. Portadas agregadas: {con_foto}. Sin portada: {sin_foto}.'
        ))
