import sys
import base64
from cryptography import fernet
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
sys.path.append('classes')
from Site import Site
from auth import auth
from mainpage import mainpage
from projects import projects
from users import users
from items import items
from components import components

app = web.Application(client_max_size=1024**100)
app.router.add_static('/system/files', path='files', name='csv')

# Установка сессий
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

SITE = Site()
SITE.debug_on = True  # Выводить отладочную информацию


@aiohttp_jinja2.template('main.html')
async def system_r(request):
    SITE.debug('===== SYSTEM =====')
    SITE.debug('REQUEST:')
    SITE.debug(request)

    SITE.initial()
    SITE.procReq(request)
    SITE.post = await request.post()  # Ждём получение файлов методом POST
    SITE.session = await get_session(request)

    # Проверка авторизации
    if not auth.auth(SITE):
        SITE.debug('Нет авторизации')
        return {'AUTH': False, 'content': SITE.content, 'head': SITE.getHead()}

    # Редирект для url авторизации
    if SITE.p[1] == 'auth':
        return web.HTTPFound('/system/')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'projects': projects.router,
        'users': users.router,
        'items': items.router,
        'com': components.router,
    }

    if (SITE.p[1] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции возвращает не False в случае редиректа
    r = functions[SITE.p[1]](SITE)

    # Проверка и обработка редиректа
    if r:
        if 'redirect' in r:
            # Обработка редиректа
            return web.HTTPFound(r['redirect'])
        if 'ajax' in r:
            # Обработка ajax
            return web.HTTPOk(text=r['ajax'])

    return {'AUTH': True, 'content': SITE.content, 'head': SITE.getHead()}


aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([
    web.static('/lib', 'lib'),
    web.static('/templates', 'templates'),
    web.static('/files', 'files'),
    web.get('/system{url:.*}', system_r),  # Админка
    web.post('/system{url:.*}', system_r),  # Админка
])

if __name__ == '__main__':
    web.run_app(app, port=9001)
