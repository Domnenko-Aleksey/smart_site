import sys
import base64
from cryptography import fernet
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import pymysql
import pymysql.cursors
import config
sys.path.append('classes')
from Site import Site
from pages import pages

# Подключаем базу данных
con = pymysql.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    db=config.db,
    charset='utf8mb4',
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

app = web.Application(client_max_size=1024**100)

# Установка сессий
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

SITE = Site()
SITE.db = con.cursor()
SITE.debug_on = True  # Выводить отладочную информацию


@aiohttp_jinja2.template('pages/index.html')
async def index(request):
    SITE.debug('===== INDEX =====')

    SITE.initial()
    SITE.procReq(request)
    SITE.post = await request.post()  # Ждём получение файлов методом POST
    SITE.session = await get_session(request)

    r = pages.router(SITE)

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
    web.get('/{url:.*}', index),  # Админка
    web.post('/{url:.*}', index),  # Админка
])

if __name__ == '__main__':
    web.run_app(app, port=9005)
