"""
Copia los datos que estaban en SQLite hacia MongoDB.

Uso:
    python manage.py migrar_a_mongo

SQLite solo se LEE, no se modifica ni se borra.
Se puede correr varias veces: borra primero lo que haya en Mongo y lo rehace.
"""

from django.core.management.base import BaseCommand

from catalogo import documents as mongo   # documentos de MongoDB
from catalogo import models as sqlite     # modelos viejos de SQLite


class Command(BaseCommand):
    help = 'Copia Generos, Autores y Libros de SQLite a MongoDB.'

    def handle(self, *args, **options):
        # 1. Limpiar Mongo para no duplicar. Libros primero: apuntan a los otros dos.
        mongo.Libro.objects().delete()
        mongo.Autor.objects().delete()
        mongo.Genero.objects().delete()

        # 2. Generos. Guardamos un mapa id_sqlite -> documento_mongo
        #    para poder rearmar las llaves foraneas mas abajo.
        mapa_generos = {}
        for g in sqlite.Genero.objects.all():
            mapa_generos[g.id] = mongo.Genero(
                nombre=g.nombre,
                descripcion=g.descripcion,
            ).save()

        # 3. Autores
        mapa_autores = {}
        for a in sqlite.Autor.objects.all():
            mapa_autores[a.id] = mongo.Autor(
                nombre=a.nombre,
                contacto=a.contacto,
            ).save()

        # 4. Libros, ya con las referencias apuntando a los documentos de Mongo.
        total_libros = 0
        for l in sqlite.Libro.objects.all():
            mongo.Libro(
                titulo=l.titulo,
                autor=mapa_autores[l.autor_id],
                genero=mapa_generos[l.genero_id],
                anio=l.anio,
                stock=l.stock,
                sinopsis=l.sinopsis,
            ).save()
            total_libros += 1

        self.stdout.write(self.style.SUCCESS(
            f'Copiado a MongoDB: {len(mapa_generos)} generos, '
            f'{len(mapa_autores)} autores, {total_libros} libros.'
        ))
