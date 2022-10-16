from aiohttp import web
from items import mainpage
from items import edit
from items import insert
from items import update
from items import status
from items import ordering
from items import delete
from items import image_upload_ajax
from items import image_delete_ajax

def router(SITE):
    SITE.debug('PATH: /system/items/items.py (router)')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'add': edit.edit,
        'edit': edit.edit,
        'insert': insert.insert,
        'update': update.update,
        'image_upload_ajax': image_upload_ajax.image_upload_ajax,
        'image_delete_ajax': image_delete_ajax.image_delete_ajax,
        'pub': status.status,
        'unpub': status.status,
        'up': ordering.ordering,
        'down': ordering.ordering,
        'delete': delete.delete
    }

    if (SITE.p[2] not in functions):
        try:
            check = int(SITE.p[2]) > 0
        except Exception:
            # Если функция не существует - 404
            raise web.HTTPNotFound()
        return functions[''](SITE)
    else:
        # Вызов функции
        return functions[SITE.p[2]](SITE)
