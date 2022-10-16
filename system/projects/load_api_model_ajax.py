import requests
import json
import config


def load_api_model_ajax(SITE):
    SITE.debug('PATH: /system/projects/load_api_model_ajax.py')
    SITE.debug(f'POST: {SITE.post}')

    # Загружаем модель в API
    project_id = SITE.post['project_id']
    param = {'token': config.api_token, 'project_id': project_id}
    api_req = requests.post('http://127.0.0.1:9007/api/load_model_ajax', data=param)
    if int(api_req.status_code) != 200:
        answer = {'answer': 'error', 'message': ''}
        return {'ajax': json.dumps(answer)} 
    answer = {'answer': 'success'}
    return {'ajax': json.dumps(answer)} 