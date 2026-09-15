# Guía: qué se hizo y dónde verlo

Tema: catálogo de la biblioteca UPB. Diseño tomado del Figma "Sipesa | Website"
(página inicial `node 740-2`, página de catálogo `node 740-86`).

## Requisitos del laboratorio

### 2. Proyecto conectado con el driver/ORM de la stack
**MongoDB Atlas** con el ODM **MongoEngine** (encima del driver `pymongo`).

MongoEngine es a MongoDB lo que el ORM de Django es a SQLite: misma idea
(clases de Python ↔ datos guardados), adaptada a documentos.

| Archivo | Qué hace |
|---------|----------|
| `.env` | usuario, contraseña y cluster. **No se sube a git.** |
| `config/mongo.py` | abre la conexión (`connect()`). Único punto de conexión. |
| `config/settings.py` (final) | llama a `conectar_mongo()` al arrancar Django. |
| `catalogo/documents.py` | los documentos: `Genero`, `Autor`, `Libro`. |

**SQLite quedó desconectado del catálogo.** El archivo `db.sqlite3` sigue ahí y
`DATABASES` sigue apuntándole, pero solo porque Django lo necesita para `/admin/`,
login y sesiones. Ninguna vista del catálogo lo toca. `catalogo/models.py` se dejó
como referencia de cómo era antes.

### 3. Al menos dos colecciones relacionadas con llave foránea
Archivo: `catalogo/documents.py` — hay **tres** colecciones:

```
Genero (1) ──< Libro >── (1) Autor
```

- `Libro.autor  = ReferenceField(Autor)`   → guarda el `_id` del autor
- `Libro.genero = ReferenceField(Genero)`  → guarda el `_id` del género

`ReferenceField` es la llave foránea de Mongo: guarda el `_id` del otro documento
y MongoEngine lo resuelve solo cuando haces `libro.autor.nombre`.

Verlo en la base: Atlas → Browse Collections → base `devweb` → colecciones
`generos`, `autores`, `libros`.

### 4. Los datos se muestran con el motor de plantillas (nada escrito a mano)
Templates en `catalogo/templates/catalogo/`:

| Template      | Qué muestra                          | De dónde sale                                          |
|---------------|--------------------------------------|--------------------------------------------------------|
| `base.html`   | header, nav y footer compartidos     | —                                                       |
| `inicio.html` | tarjetas de género + conteo de libros| `_generos_con_conteo()` en `views.py`                  |
| `listado.html`| grid de libros del género            | `Libro.objects(genero=genero)`                         |
| `detalle.html`| ficha del libro + relacionados       | `Libro.objects.get(pk=...)`                            |

El chip "N Libros" del inicio es el conteo real de la referencia, no un número fijo.
Si agregás un libro en Atlas, la vista cambia sola.

Los templates no cambiaron nada: `libro.id` funciona igual en MongoEngine.
Lo único que cambió fue `catalogo/urls.py`: `<int:...>` → `<str:...>`, porque los
ids de Mongo son `ObjectId` (texto tipo `68a4bc...`), no enteros.

## Rutas

| URL                            | Vista               | Pantalla del Figma |
|--------------------------------|---------------------|--------------------|
| `/`                            | `views.inicio`      | página inicial     |
| `/catalogo/`                   | `views.catalogo`    | catálogo completo  |
| `/catalogo/genero/<id>/`       | `views.catalogo`    | catálogo por género|
| `/libro/<id>/`                 | `views.detalle`     | (extra) detalle    |
| `/admin/`                      | admin de Django     | —                  |

## Datos

6 géneros, 12 autores, 17 libros — se copiaron de SQLite a MongoDB con:

```
python manage.py migrar_a_mongo
```

Ese comando está en `catalogo/management/commands/migrar_a_mongo.py`.
Solo **lee** SQLite, no lo modifica. Se puede correr las veces que quieras:
borra lo que haya en Mongo y lo vuelve a copiar.

## Cómo levantarlo desde cero

```
python -m pip install "pymongo[srv]" mongoengine python-dotenv
copy .env.example .env      # y poner las credenciales reales
python manage.py migrar_a_mongo
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`.
