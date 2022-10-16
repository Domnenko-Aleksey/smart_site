from aiohttp import web
from components.search.sites import mainpage
from components.search.sites import edit
from components.search.sites import insert
from components.search.sites import update
from components.search.sites import status
from components.search.sites import ordering
from components.search.sites import delete
from components.search.sites import scan_sitemap_ajax
from components.search.sites import scan_page_ajax
from components.search.sites import search_test

def router(SITE):
    SITE.debug('PATH: /system/components/search/sites/router.py')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'add': edit.edit,
        'edit': edit.edit,
        'insert': insert.insert,
        'update': update.update,
        'pub': status.status,
        'unpub': status.status,
        'up': ordering.ordering,
        'down': ordering.ordering,
        'delete': delete.delete,
        'search_test': search_test.search_test,
        'scan_sitemap_ajax': scan_sitemap_ajax.scan_sitemap_ajax,
        'scan_page_ajax': scan_page_ajax.scan_page_ajax,
    }

    if (SITE.p[4] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[4]](SITE)