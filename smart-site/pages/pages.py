from aiohttp import web
from pages.mainpage import mainpage

def router(SITE):
    SITE.debug('PATH: /pages/pages.py')

    functions = {
        '': mainpage.mainpage,
    }

    if (SITE.p[0] not in functions):
        raise web.HTTPNotFound()

    return functions[SITE.p[0]](SITE)

