from aiohttp import web
from users import mainpage
from users import edit
from users import insert
from users import update
from users import status
from users import ordering
from users import delete


def router(SITE):
    SITE.debug('PATH: /system/users/users.py (router)')

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
        'delete': delete.delete
    }

    if (SITE.p[2] not in functions):
        # Если функция не существует - 404
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[2]](SITE)
