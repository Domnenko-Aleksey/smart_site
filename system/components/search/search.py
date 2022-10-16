from aiohttp import web
from components.search.sites import sites
from components.search.pages import pages

def router(SITE):
    SITE.debug('PATH: /system/components/search/router.py (router)')

    # Вызов функций по ключу
    functions = {
        '': sites.router,
        'sites': sites.router,
        'pages': pages.router,
    }

    if (SITE.p[3] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[3]](SITE)