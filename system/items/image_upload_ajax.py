import json
import os
import uuid  # Уникальное имя для файла
from Items import Items


def image_upload_ajax(SITE):
    SITE.debug('PATH: /system/items/image_upload_ajax.py')

    id = SITE.post['id']
    file = SITE.post['file'].file.read()
    post_file_name = SITE.post['file'].filename.lower()
    ext = post_file_name.split('.')[-1]
    
    file_name = uuid.uuid4().hex + '.' + ext

    # Получаем данные для топика
    ITEM = Items(SITE)
    item = ITEM.getItem(id)
    item['content']['images'].append(file_name)
    
    path = '../files/projects/'+str(item['project_id'])+'/'+str(id)

    if not os.path.isdir(path):
        os.mkdir(path, mode=0o755)

    # Сохраняем файл
    with open(path + '/' + file_name, 'wb') as f:
        f.write(file)
    
    ITEM.update(item)

    answer = {'answer': 'success', 'file_name': file_name, 'project_id': item['project_id']}
    return {'ajax': json.dumps(answer)}