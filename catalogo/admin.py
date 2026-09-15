"""
El admin de Django solo sabe hablar con SQLite/PostgreSQL, no con MongoDB.
Como Genero/Autor/Libro se mudaron a Mongo (catalogo/documents.py), se dejan
de registrar aqui: si no, /admin/ mostraria los datos viejos de SQLite.

El panel /admin/ sigue funcionando para usuarios y grupos de Django.
"""

# from django.contrib import admin
# from .models import Autor, Genero, Libro   # <- viven en SQLite, desconectados
