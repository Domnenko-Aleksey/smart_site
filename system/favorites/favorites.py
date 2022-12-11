from aiohttp import web
from favorites import mainpage

def router(SITE):
    SITE.debug('PATH: /system/favorites/favorites.py (router)')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
    }

    if (SITE.p[2] not in functions):
        try:
            check = int(SITE.p[2]) > 0
        except Exception:
            raise web.HTTPNotFound()
        return functions[''](SITE)
    else:
        return functions[SITE.p[2]](SITE)
