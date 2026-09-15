from django.db import migrations


GENEROS = [
    ('Aventura', 'Viajes, expediciones y riesgo.'),
    ('Ciencia Ficción', 'Futuros posibles y tecnología.'),
    ('Realismo mágico', 'Lo cotidiano con un giro imposible.'),
    ('Distopía', 'Sociedades bajo control.'),
    ('Fantasía', 'Mundos con reglas propias.'),
    ('Clásicos', 'Obras que sostienen el canon.'),
]

AUTORES = [
    ('Gabriel García Márquez', 'gabo@editorial.com'),
    ('J.K. Rowling', 'jk@editorial.com'),
    ('George Orwell', 'orwell@editorial.com'),
    ('J.R.R. Tolkien', 'tolkien@editorial.com'),
    ('Julio Verne', 'verne@editorial.com'),
    ('Isaac Asimov', 'asimov@editorial.com'),
    ('Frank Herbert', 'herbert@editorial.com'),
    ('Robert L. Stevenson', 'stevenson@editorial.com'),
    ('Aldous Huxley', 'huxley@editorial.com'),
    ('Miguel de Cervantes', 'cervantes@editorial.com'),
    ('Homero', 'homero@editorial.com'),
    ('Ursula K. Le Guin', 'leguin@editorial.com'),
]

# (titulo, autor, genero, anio, stock, sinopsis)
LIBROS = [
    ('La isla del tesoro', 'Robert L. Stevenson', 'Aventura', 1883, 4,
     'Un mapa, un motín y un pirata con demasiada labia.'),
    ('Veinte mil leguas de viaje submarino', 'Julio Verne', 'Aventura', 1870, 2,
     'El Nautilus recorre el océano al mando del capitán Nemo.'),
    ('La vuelta al mundo en 80 días', 'Julio Verne', 'Aventura', 1872, 0,
     'Una apuesta imposible contra el reloj y la geografía.'),
    ('El hobbit', 'J.R.R. Tolkien', 'Aventura', 1937, 6,
     'Un viaje a la Montaña Solitaria que nadie pidió.'),
    ('Fundación', 'Isaac Asimov', 'Ciencia Ficción', 1951, 3,
     'La psicohistoria intenta acortar treinta mil años de caos.'),
    ('Yo, robot', 'Isaac Asimov', 'Ciencia Ficción', 1950, 0,
     'Nueve relatos donde las tres leyes fallan de formas elegantes.'),
    ('Dune', 'Frank Herbert', 'Ciencia Ficción', 1965, 5,
     'Especia, desierto y política en Arrakis.'),
    ('La mano izquierda de la oscuridad', 'Ursula K. Le Guin', 'Ciencia Ficción', 1969, 2,
     'Un planeta helado donde el género no es fijo.'),
    ('Cien años de soledad', 'Gabriel García Márquez', 'Realismo mágico', 1967, 5,
     'Macondo y los Buendía, de la fundación al olvido.'),
    ('El amor en los tiempos del cólera', 'Gabriel García Márquez', 'Realismo mágico', 1985, 1,
     'Cincuenta y tres años esperando una respuesta.'),
    ('1984', 'George Orwell', 'Distopía', 1949, 3,
     'El Gran Hermano vigila incluso lo que no dijiste.'),
    ('Rebelión en la granja', 'George Orwell', 'Distopía', 1945, 0,
     'Los animales toman la granja; después toman todo lo demás.'),
    ('Un mundo feliz', 'Aldous Huxley', 'Distopía', 1932, 4,
     'Felicidad garantizada, siempre que no preguntes.'),
    ('El señor de los anillos', 'J.R.R. Tolkien', 'Fantasía', 1954, 0,
     'Un anillo, una montaña de fuego y muchísimo caminar.'),
    ('Harry Potter y la piedra filosofal', 'J.K. Rowling', 'Fantasía', 1997, 8,
     'Un niño descubre que la carta sí era para él.'),
    ('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Clásicos', 1605, 2,
     'Leer demasiado también tiene consecuencias.'),
    ('La Odisea', 'Homero', 'Clásicos', 1927, 3,
     'Diez años para volver a casa, con desvíos.'),
]


def crear_datos(apps, schema_editor):
    Autor = apps.get_model('catalogo', 'Autor')
    Genero = apps.get_model('catalogo', 'Genero')
    Libro = apps.get_model('catalogo', 'Libro')

    generos = {n: Genero.objects.create(nombre=n, descripcion=d) for n, d in GENEROS}
    autores = {n: Autor.objects.create(nombre=n, contacto=c) for n, c in AUTORES}

    for titulo, autor, genero, anio, stock, sinopsis in LIBROS:
        Libro.objects.create(
            titulo=titulo,
            autor=autores[autor],
            genero=generos[genero],
            anio=anio,
            stock=stock,
            sinopsis=sinopsis,
        )


def borrar_datos(apps, schema_editor):
    for modelo in ('Libro', 'Autor', 'Genero'):
        apps.get_model('catalogo', modelo).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos, borrar_datos),
    ]
