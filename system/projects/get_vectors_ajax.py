import requests
import json
import numpy as np
from Items import Items
from tensorflow.keras.utils import to_categorical

def get_vectors_ajax(SITE):
    SITE.debug('PATH: /system/items/get_vectors_ajax.py')

    if SITE.model['item_current'] >= SITE.model['items_count']:
        answer = {
            'answer': 'success', 
            'items_count': SITE.model['items_count'], 
            'item_current': SITE.model['item_current'], 
            'message': 'Обработка данных завершена',
            'finish': 'Ok'
        }
        return {'ajax': json.dumps(answer)}

    item = SITE.model['items_list'][SITE.model['item_current']]

    SITE.debug('ITEM:')
    SITE.debug(item)

    ITEM = Items(SITE)
    ITEM.updateIdx(item['id'], SITE.model['item_current'])
    item_questions = item['questions'].split(';')
    for q in item_questions:
        # BERT REST API для каждого запроса
        param = {'text': q}
        bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
        if int(bert_req.status_code) != 200:
            return json.dumps({'answer': 'error', 'message': ''})
        vector = bert_req.json()['vector']
        SITE.model['x'].append(vector)
        y_cat = to_categorical(SITE.model['item_current'], num_classes=SITE.model['items_count'], dtype='int')
        SITE.model['y'].append(y_cat)
    SITE.model['item_current'] += 1

    SITE.debug(f'ВЕКТОР, РАЗМЕР: {len(vector)}')
    SITE.debug(f'ДЛИНА СПИСКА: {len(SITE.model["x"])}, ТЕКУЩИЙ ИНДЕКС: {SITE.model["item_current"]}, ВСЕГО: {SITE.model["items_count"]}')

    message = f'Топик: <i>"{item["name"]}"</i>, вопросов: {str(len(q))}'
    finish = ''

    answer = {
        'answer': 'success', 
        'items_count': SITE.model['items_count'], 
        'item_current': SITE.model['item_current'], 
        'message': message,
        'finish': finish
    }
    return {'ajax': json.dumps(answer)}

