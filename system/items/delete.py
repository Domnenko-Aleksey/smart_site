import os
from Items import Items

def delete(SITE):
    print('PATH: /system/items/delete.py')
    id = SITE.p[3]
    ITEM = Items(SITE)
    item = ITEM.getItem(id)

    # Удаляем файлы
    if item['content']['images']:
        for file_name in item['content']['images']:
            path = '../files/projects/' + str(item['project_id']) + '/' + file_name
            if os.path.isfile(path):
                os.remove(path)

    ITEM.delete(id)

    return {'redirect': '/system/items/'+str(item['project_id'])}