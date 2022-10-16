from aiohttp import web
from components.search.pages import mainpage

def router(SITE):
    SITE.debug('PATH: /system/components/search/pages/router.py')

    functions = {
        'list': mainpage.mainpage,
    }

    if (SITE.p[4] not in functions):
        raise web.HTTPNotFound()

    return functions[SITE.p[4]](SITE)