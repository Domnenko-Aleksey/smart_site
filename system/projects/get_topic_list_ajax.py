import json
from Items import Items


'''
SITE.model['project_id'] -> устанавливаем project_id, признак того, что модель этого проекта в обработке
SITE.model['items_list'] -> список items по project_id
SITE.model['items_count'] -> количество топиков
SITE.model['item_current'] -> текущий топик
SITE.model['vectors_list'] -> список векторов [vector, item_current]
SITE.model['model'] -> модель классификации
'''


def get_topic_list_ajax(SITE):
    SITE.debug('PATH: /system/items/get_topic_list_ajax.py')

    SITE.model['epochs_count'] = int(SITE.post['epochs_count'])

    if not SITE.model['project_id']:
        # Если проект не был запущен ранее
        SITE.model['project_id'] = SITE.post['project_id']
        ITEM = Items(SITE)
        sql_select = 'id, name, questions, status'

        SITE.model['items_list'] = ITEM.getItemList(SITE.model['project_id'], sql_select, status=1)
        SITE.model['items_count'] = len(SITE.model['items_list'])
        message = f'Начата обработка данных проекта {SITE.model["project_id"]}'
    else:
        message = f'Продолжаем обработку данных проекта {SITE.model["project_id"]}'       

    SITE.debug(f'PROJECT ID: {SITE.model["project_id"]}, КОЛИЧЕСТВО ТОПИКОВ: {SITE.model["items_count"]}')

    answer = {
        'answer': 'success', 
        'project_id': SITE.model['project_id'], 
        'items_count': SITE.model['items_count'],
        'item_current': SITE.model['item_current'],
        'message': message
    }
    return {'ajax': json.dumps(answer)}