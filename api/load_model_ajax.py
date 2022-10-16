import json
import config 
from ClsModel import ClsModel

# Загружает модель по ajax запросу
def load_model_ajax(SITE):
    SITE.debug('PATH: /api/load_model_ajax.py')
    SITE.debug(f'POST: {SITE.post}')
    
    if 'token' not in SITE.post or SITE.post['token'] != config.token:
        SITE.debug('Ошибка доступа')
        return
    project_id = int(SITE.post['project_id'])
    CLS_MODEL = ClsModel(SITE.db)
    SITE.models[project_id] = CLS_MODEL.loadModel(project_id)
    SITE.debug(f'МОДЕЛИ: {SITE.models}')

    return json.dumps({'answer': 'success'})