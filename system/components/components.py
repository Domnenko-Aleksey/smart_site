from aiohttp import web
from components.search import search

def router(SITE):
    SITE.debug('PATH: /system/components/router.py (router)')

    # Вызов функций по ключу
    functions = {
        'search': search.router,
    }

    if (SITE.p[2] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[2]](SITE)
