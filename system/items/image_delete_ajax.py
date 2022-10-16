import json
import os
from Items import Items


def image_delete_ajax(SITE):
    SITE.debug('PATH: /system/items/image_delete_ajax.py')

    id = SITE.post['id']
    file_name = SITE.post['file_name']
    
    # Получаем данные для топика
    ITEM = Items(SITE)
    item = ITEM.getItem(id)
    
    if file_name in item['content']['images']:
        item['content']['images'].remove(file_name)
    
    path = '../files/projects/'+str(item['project_id']) + '/' + str(id) + '/' + file_name

    # Удаляем файл
    if os.path.isfile(path):
        os.remove(path)
    
    ITEM.update(item)

    answer = {'answer': 'success'}
    return {'ajax': json.dumps(answer)}