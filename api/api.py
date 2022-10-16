import random
import sys
from aiohttp import web
sys.path.append('classes')
from Site import Site
from ClsModel import ClsModel

import get_title_ajax
import get_speech_answer_ajax
import get_id_answer_ajax
import get_fav_ajax
import set_fav_ajax
import load_model_ajax


app = web.Application(client_max_size=1024**100)

SITE = Site()
SITE.debug_on = True  # Выводить отладочную информацию

# Загрузка моделей
CLS_MODEL = ClsModel(SITE.db)
SITE.models = CLS_MODEL.loadModel()
SITE.debug('ЗАГРУЖЕНЫ МОДЕЛИ')
SITE.debug(SITE.models)


async def index(request):
    SITE.debug('===== INDEX =====')
    SITE.initial()
    SITE.procReq(request)
    SITE.post = await request.post()  # Ждём получение файлов методом POST

    functions = {
        'get_title_ajax': get_title_ajax.get_title_ajax,
        'get_id_answer_ajax': get_id_answer_ajax.get_id_answer_ajax,
        'get_speech_answer_ajax': get_speech_answer_ajax.get_speech_answer_ajax,
        'get_fav_ajax': get_fav_ajax.get_fav_ajax,
        'set_fav_ajax': set_fav_ajax.set_fav_ajax,
        'load_model_ajax': load_model_ajax.load_model_ajax,
    }

    if (SITE.p[1] not in functions):
        raise web.HTTPNotFound()

    r = functions[SITE.p[1]](SITE)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }

    return web.Response(text=r, headers=headers)


app.add_routes([
    web.get('/{url:.*}', index),  # Админка
    web.post('/{url:.*}', index),  # Админка
])


if __name__ == '__main__':
    web.run_app(app, port=9007)
