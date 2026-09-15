"""
Documentos de MongoDB (equivalente a catalogo/models.py, pero para Mongo).

Tabla en SQL  ->  Coleccion en Mongo
Fila          ->  Documento
models.Model  ->  mongoengine.Document
ForeignKey    ->  ReferenceField

catalogo/models.py sigue existiendo pero ya no lo usan las vistas: quedo
desconectado, solo como referencia de como era en SQLite.
"""

from mongoengine import (
    CASCADE,
    DENY,
    Document,
    EmailField,
    IntField,
    ReferenceField,
    StringField,
)


class Genero(Document):
    """Categoria del catalogo. Cada Libro pertenece a un Genero."""

    nombre = StringField(max_length=80, required=True, unique=True)
    descripcion = StringField(max_length=200, default='')

    # meta reemplaza a "class Meta" de Django.
    meta = {
        'collection': 'generos',   # nombre de la coleccion en Mongo
        'ordering': ['nombre'],
    }

    def __str__(self):
        return self.nombre


class Autor(Document):
    nombre = StringField(max_length=100, required=True)
    contacto = EmailField()

    meta = {
        'collection': 'autores',
        'ordering': ['nombre'],
    }

    def __str__(self):
        return self.nombre


class Libro(Document):
    titulo = StringField(max_length=150, required=True)

    # ReferenceField = la llave foranea de Mongo.
    # Guarda el _id del Autor y MongoEngine lo resuelve al leerlo.
    autor = ReferenceField(Autor, required=True, reverse_delete_rule=CASCADE)
    genero = ReferenceField(Genero, required=True, reverse_delete_rule=DENY)

    anio = IntField(required=True)
    stock = IntField(default=0)
    sinopsis = StringField(default='')

    meta = {
        'collection': 'libros',
        'ordering': ['titulo'],
    }

    def __str__(self):
        return self.titulo

    @property
    def disponible(self):
        return self.stock > 0
