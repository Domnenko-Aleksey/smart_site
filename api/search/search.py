from aiohttp import web
from search import get_search

def router(SITE):
    SITE.debug('PATH: /api/search/search.py (router)')

    # Вызов функций по ключу
    functions = {
        # 'load_model': model_load.model_load,
        'get_search': get_search.get_search
    }

    if (SITE.p[2] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[2]](SITE)