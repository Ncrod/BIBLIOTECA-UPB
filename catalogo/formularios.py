"""
Validación del formulario de libros (crear/editar).

Responsabilidad única de este archivo: decidir si los datos que mandó
el usuario son válidos. No sabe nada de HTTP (no toca request ni
response) y no guarda nada en la base de datos — solo lee libros/
autores/géneros a través de repositorios.py para comprobar que existen.
"""

from . import repositorios


def limpiar_libro(datos):
    """
    datos: algo tipo diccionario con lo que mandó el formulario
    (normalmente request.POST).

    Regresa (limpios, errores):
        limpios: dict listo para pasarle a repositorios.guardar_libro(**limpios)
        errores: lista de mensajes en español, vacía si todo está bien
    """
    errores = []
    limpios = {}

    limpios['titulo'] = datos.get('titulo', '').strip()
    if not limpios['titulo']:
        errores.append('El título es obligatorio.')

    autor_id = datos.get('autor')
    limpios['autor'] = None
    if autor_id:
        try:
            limpios['autor'] = repositorios.obtener_autor(autor_id)
        except repositorios.NoEncontrado:
            errores.append('El autor seleccionado no existe.')
    else:
        errores.append('Debes elegir un autor.')

    genero_id = datos.get('genero')
    limpios['genero'] = None
    if genero_id:
        try:
            limpios['genero'] = repositorios.obtener_genero(genero_id)
        except repositorios.NoEncontrado:
            errores.append('El género seleccionado no existe.')
    else:
        errores.append('Debes elegir un género.')

    try:
        limpios['anio'] = int(datos.get('anio', '').strip())
    except ValueError:
        errores.append('El año debe ser un número.')
        limpios['anio'] = None

    stock = datos.get('stock', '').strip()
    try:
        limpios['stock'] = int(stock) if stock else 0
    except ValueError:
        errores.append('El stock debe ser un número.')
        limpios['stock'] = None

    limpios['sinopsis'] = datos.get('sinopsis', '').strip()

    return limpios, errores
