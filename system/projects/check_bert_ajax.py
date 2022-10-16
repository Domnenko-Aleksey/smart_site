import requests
import json
import time

def check_bert_ajax(SITE):
    SITE.debug('PATH: /system/items/check_bert_ajax.py')

    start_time = time.time()
    param = {'text': 'ТЕСТ BERT МОДЕЛИ'}

    try:
        bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
        if int(bert_req.status_code) != 200:
            answer = {
                'answer': 'success', 
                'content': '<div style="color:#ff0000">Ошибка подключения!</div>'
            }      
            return {'ajax': json.dumps(answer)}

        vector = bert_req.json()['vector']
        delta_time = time.time() - start_time
        answer = {
            'answer': 'success', 
            'content': f'<div>Проверка BERT, <br>время выполнения: {round(delta_time, 4)} с, <br>вектор: {len(vector)}</div>'
        } 
        return {'ajax': json.dumps(answer)}
    except:
        answer = {
            'answer': 'success', 
            'content': '<div style="color:#ff0000">Ошибка подключения!</div>'
        }
        return {'ajax': json.dumps(answer)}       