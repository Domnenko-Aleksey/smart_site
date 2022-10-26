from aiohttp import web
from sections import edit
from sections import insert
from sections import update
from sections import ordering
from sections import delete


def router(SITE):
    SITE.debug('PATH: /system/sections/sections.py (router)')

    # Вызов функций по ключу
    functions = {
        'add': edit.edit,
        'edit': edit.edit,
        'insert': insert.insert,
        'update': update.update,
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
