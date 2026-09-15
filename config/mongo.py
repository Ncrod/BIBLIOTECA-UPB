"""
Conexión a MongoDB Atlas.

Aquí y solo aquí se abre la conexión con la base. Se llama una vez desde
config/settings.py, cuando Django arranca.

Idea clave: MongoEngine es a MongoDB lo que el ORM de Django es a SQLite.
Mismo concepto (clases de Python <-> datos guardados), adaptado a documentos.
"""

import os

from dotenv import load_dotenv
from mongoengine import connect

# Lee el archivo .env y mete sus valores en las variables de entorno.
# Así la contraseña nunca queda escrita dentro del código.
load_dotenv()


def conectar_mongo():
    """Abre la conexión con el cluster de Atlas. Se llama al arrancar Django."""
    uri = os.getenv('MONGODB_URI')
    nombre_db = os.getenv('MONGODB_DB', 'devweb')

    if not uri:
        raise RuntimeError(
            'Falta MONGODB_URI. Copia .env.example a .env y pon tus credenciales.'
        )

    # connect() registra la conexión con el alias 'default'.
    # Todos los Document de catalogo/documents.py la usan automáticamente.
    return connect(db=nombre_db, host=uri, alias='default')
