"""
MODELOS DE SQLITE - DESCONECTADOS.

Este archivo ya NO lo usan las vistas. Los datos del catalogo ahora viven
en MongoDB: ver catalogo/documents.py.

Se deja aqui solo como referencia, para comparar como se veia lo mismo
con el ORM de Django y con MongoEngine.
"""

from django.db import models


class Genero(models.Model):
    """Categoría del catálogo. Cada Libro pertenece a un Género (llave foránea)."""
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Géneros'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    """Campo anidado: cada Libro tiene un Autor con su propia info."""
    nombre = models.CharField(max_length=100)
    contacto = models.EmailField()

    class Meta:
        verbose_name_plural = 'Autores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name='libros')
    anio = models.IntegerField(verbose_name='Año')
    stock = models.IntegerField(default=0)
    sinopsis = models.TextField(blank=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    @property
    def disponible(self):
        return self.stock > 0
