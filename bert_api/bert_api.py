import sys
import json
import numpy as np
import pymysql
import pymysql.cursors
from aiohttp import web
from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text
import config
sys.path.append('classes')
from Core import Core

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

CORE = Core()
CORE.db = con.cursor()

# Получаем список разрешённых ip адресов
allowed_ip = CORE.get_allowed_ip()
CORE.allowed_ip = allowed_ip + config.allowed_ip
print('ALLOWED API:', CORE.allowed_ip)

# Модель BERT находится по адресу './model/bert_pt_model.h5'
# Модель включает в себя компиляцию 2х моделей - 'bert_preprocess' + 'bert_encoder'
# Нв вход модели подаётся текст, на выходе получаем вектоp с размерностью (1, 768)
# Модель - многоязычная
path = './model/bert_pt_model.h5' 
model = keras.models.load_model(path, custom_objects={'KerasLayer': hub.KerasLayer})


app = web.Application(client_max_size=1024**100)


async def bert_api(request):
    # print('===== BERT API =====')
    # print('ALLOWED IP', CORE.allowed_ip, 'REMOTE IP:', request.remote)

    # Разрешённый список ip адресов
    if request.remote not in CORE.allowed_ip:
        answer = {'answer': 'error', 'message': 'Not allowed'}
        return web.HTTPOk(text=json.dumps(answer))

    post = await request.post()  # Ждём получение файлов методом POST
    # print('POST', post)

    # Метод POST
    if request.method == 'POST':
        if 'text' not in post:
            answer = {'answer': 'error', 'message': 'Bad request'}
        else:
            if len(post['text']) < 3:
                answer = {'answer': 'error', 'message': 'Short text'}
            else:
                predict = model.predict([post['text']])
                # print('PREDICT SHAPE:', predict.shape)
                vector = predict[0].tolist()
                answer = {'answer': 'success', 'vector': vector}
    else:
        answer = {'answer': 'success', 'message': 'method GET'}

    return web.HTTPOk(text=json.dumps(answer))


app.add_routes([
    web.get('/bert_api{url:.*}', bert_api),
    web.post('/bert_api{url:.*}', bert_api),
])

if __name__ == '__main__':
    web.run_app(app, port=9003)
