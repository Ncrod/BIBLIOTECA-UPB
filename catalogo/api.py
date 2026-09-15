import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import formularios, repositorios


def serializar_autor(autor):
    return {
        'id': str(autor.id),
        'nombre': autor.nombre,
        'contacto': autor.contacto,
    }


def serializar_genero(genero):
    datos = {
        'id': str(genero.id),
        'nombre': genero.nombre,
        'descripcion': genero.descripcion,
    }

    if hasattr(genero, 'total_libros'):
        datos['total_libros'] = genero.total_libros

    return datos


def serializar_libro(libro):
    return {
        'id': str(libro.id),
        'titulo': libro.titulo,
        'autor': serializar_autor(libro.autor),
        'genero': serializar_genero(libro.genero),
        'anio': libro.anio,
        'stock': libro.stock,
        'sinopsis': libro.sinopsis,
        'disponible': libro.disponible,
    }


def respuesta_error(mensaje, estado=400, errores=None):
    datos = {'error': mensaje}
    if errores is not None:
        datos['errores'] = errores
    return JsonResponse(datos, status=estado)


def datos_request(request):
    if request.content_type == 'application/json':
        try:
            datos = json.loads(request.body.decode('utf-8') or '{}')
        except json.JSONDecodeError:
            return None, respuesta_error('JSON invalido.')

        if not isinstance(datos, dict):
            return None, respuesta_error('El cuerpo JSON debe ser un objeto.')

        return normalizar_datos(datos), None

    return request.POST, None


def normalizar_datos(datos):
    """Convierte valores JSON a strings compatibles con limpiar_libro()."""
    return {
        clave: '' if valor is None else str(valor)
        for clave, valor in datos.items()
    }


@require_http_methods(['GET'])
def api_generos(request):
    generos = repositorios.listar_generos_con_conteo()
    return JsonResponse({
        'resultados': [serializar_genero(genero) for genero in generos],
    })


@require_http_methods(['GET'])
def api_autores(request):
    autores = repositorios.listar_autores()
    return JsonResponse({
        'resultados': [serializar_autor(autor) for autor in autores],
    })


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_libros(request):
    if request.method == 'GET':
        genero_id = request.GET.get('genero')
        genero = None

        if genero_id:
            try:
                genero = repositorios.obtener_genero(genero_id)
            except repositorios.NoEncontrado:
                return respuesta_error('Genero no encontrado.', estado=404)

        libros = repositorios.listar_libros(genero=genero)
        return JsonResponse({
            'resultados': [serializar_libro(libro) for libro in libros],
        })

    datos, error = datos_request(request)
    if error:
        return error

    limpios, errores = formularios.limpiar_libro(datos)
    if errores:
        return respuesta_error('Datos invalidos.', errores=errores)

    try:
        libro = repositorios.guardar_libro(repositorios.libro_nuevo(), **limpios)
    except repositorios.DatosInvalidos as exc:
        return respuesta_error(str(exc))

    return JsonResponse(serializar_libro(libro), status=201)


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_libro_detalle(request, libro_id):
    try:
        libro = repositorios.obtener_libro(libro_id)
    except repositorios.NoEncontrado:
        return respuesta_error('Libro no encontrado.', estado=404)

    if request.method == 'GET':
        return JsonResponse(serializar_libro(libro))

    if request.method == 'DELETE':
        repositorios.eliminar_libro(libro)
        return JsonResponse({'mensaje': 'Libro eliminado.'})

    datos, error = datos_request(request)
    if error:
        return error

    if request.method == 'PATCH':
        datos_actuales = {
            'titulo': libro.titulo,
            'autor': str(libro.autor.id),
            'genero': str(libro.genero.id),
            'anio': str(libro.anio),
            'stock': str(libro.stock),
            'sinopsis': libro.sinopsis,
        }
        datos_actuales.update(datos)
        datos = datos_actuales

    limpios, errores = formularios.limpiar_libro(datos)
    if errores:
        return respuesta_error('Datos invalidos.', errores=errores)

    try:
        libro = repositorios.guardar_libro(libro, **limpios)
    except repositorios.DatosInvalidos as exc:
        return respuesta_error(str(exc))

    return JsonResponse(serializar_libro(libro))
